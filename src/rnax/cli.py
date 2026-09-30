from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from rnax.config import AnalysisConfig

app = typer.Typer(help="RNA-seq Explorer: Reproducible bulk RNA-seq differential-expression analysis.")

@app.callback()
def main() -> None:
    """RNA-seq Explorer: Reproducible bulk RNA-seq differential-expression analysis."""

@app.command()
def analyze(
    config: Annotated[
        Path, 
        typer.Option(
            "--config", 
            "-c", 
            help="Path to the analysis YAML configuration file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        )
    ],
    counts: Annotated[
        Path | None,
        typer.Option(
            "--counts",
            help="Path to the counts CSV file. Overrides config if provided.",
        )
    ] = None,
    metadata: Annotated[
        Path | None,
        typer.Option(
            "--metadata",
            help="Path to the metadata CSV file. Overrides config if provided.",
        )
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Path to the output directory. Overrides config if provided.",
        )
    ] = None,
) -> None:
    """
    Run the exploratory RNA-seq differential expression workflow.
    """
    from pandera.errors import SchemaError

    from rnax.pipeline.deseq import run_deseq2
    from rnax.pipeline.ingest import ingest_data
    
    try:
        cfg = AnalysisConfig.from_yaml(config)
        
        # Override with CLI arguments if provided
        if counts is not None:
            cfg.input.counts = counts
        if metadata is not None:
            cfg.input.metadata = metadata
        if output is not None:
            cfg.output.directory = output
            
        typer.echo(f"Successfully parsed configuration from {config}")
        
        counts_df, metadata_df = ingest_data(cfg)
        typer.echo(f"Successfully validated {counts_df.shape[0]} genes across {counts_df.shape[1]} samples.")
        
        warnings = cfg.validate_design_matrix(metadata_df)
        for w in warnings:
            typer.secho(f"Warning: {w}", fg=typer.colors.YELLOW)
            
        from rnax.manifest import build_manifest
        manifest = build_manifest(cfg, config)
        
        from rnax.pipeline.report import generate_report
        
        if cfg.contrasts and len(cfg.contrasts) > 0:
            typer.echo(f"Running multiple contrasts: {[c.name for c in cfg.contrasts]}")
            for contrast in cfg.contrasts:
                typer.echo(f"  -> Running contrast: {contrast.name}")
                norm_counts, results, filtering = run_deseq2(counts_df, metadata_df, cfg, contrast_spec=contrast)
                out_dir = Path(cfg.output.directory) / contrast.name
                generate_report(cfg, counts_df, metadata_df, norm_counts, results, manifest, filtering, contrast_spec=contrast, output_dir=out_dir)
                
            # generate index.html
            from jinja2 import Environment, FileSystemLoader
            template_dir = Path(__file__).parent / "templates"
            env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=True)
            template = env.get_template("index.html.j2")
            index_html = template.render(config=cfg)
            out_root = Path(cfg.output.directory)
            out_root.mkdir(parents=True, exist_ok=True)
            (out_root / "index.html").write_text(index_html)
            
            typer.echo("Multi-contrast analysis complete.")
        else:
            typer.echo("Running single contrast differential expression analysis...")
            norm_counts, results, filtering = run_deseq2(counts_df, metadata_df, cfg)
            
            typer.echo("Generating report and plots...")
            generate_report(cfg, counts_df, metadata_df, norm_counts, results, manifest, filtering)
            
            typer.echo(f"Differential expression complete. {results.shape[0]} genes analyzed.")
            
        typer.echo(f"Output saved to: {cfg.output.directory}")
        
    except FileNotFoundError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    except ValidationError as e:
        typer.secho(f"Configuration validation error in {config}:", fg=typer.colors.RED, err=True)
        typer.echo(e, err=True)
        raise typer.Exit(code=1)
    except SchemaError as e:
        typer.secho("Data validation error:", fg=typer.colors.RED, err=True)
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.secho("Data error:", fg=typer.colors.RED, err=True)
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
