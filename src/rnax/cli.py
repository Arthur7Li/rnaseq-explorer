from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from rnax.config import AnalysisConfig

app = typer.Typer(help="RNA-seq Explorer: Reproducible bulk RNA-seq differential-expression analysis.")

@app.callback()
def main():
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
):
    """
    Run the exploratory RNA-seq differential expression workflow.
    """
    from pandera.errors import SchemaError

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
        
        counts_df, _metadata_df = ingest_data(cfg)
        typer.echo(f"Successfully validated {counts_df.shape[0]} genes across {counts_df.shape[1]} samples.")
        
        typer.echo(f"Output will be saved to: {cfg.output.directory}")
        typer.echo("Pipeline execution is not yet fully implemented.")
        
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
