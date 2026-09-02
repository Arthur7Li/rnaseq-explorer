import yaml
from typer.testing import CliRunner

from rnax.cli import app

runner = CliRunner()


import re


def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def test_analyze_help():
    result = runner.invoke(app, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Run the exploratory RNA-seq differential expression workflow" in strip_ansi(result.output)

def test_analyze_with_valid_config(valid_config_file):
    result = runner.invoke(app, ["analyze", "--config", str(valid_config_file)])
    assert result.exit_code == 0
    assert "Successfully parsed configuration" in strip_ansi(result.output)

def test_analyze_missing_config():
    result = runner.invoke(app, ["analyze"])
    # Typer will exit 2 on missing required arguments by default
    assert result.exit_code == 2
    assert "Missing option '--config'" in strip_ansi(result.output)

def test_analyze_invalid_config(temp_dir):
    config_path = temp_dir / "bad.yaml"
    with open(config_path, "w") as f:
        yaml.dump({"invalid": "yes"}, f)
        
    result = runner.invoke(app, ["analyze", "--config", str(config_path)])
    assert result.exit_code == 1
    assert "Configuration validation error" in strip_ansi(result.output)

def test_analyze_config_not_found():
    result = runner.invoke(app, ["analyze", "--config", "does_not_exist.yaml"])
    assert result.exit_code == 2
    plain = strip_ansi(result.output).replace('\n', '').replace(' ', '')
    assert "does_not_exist.yaml" in plain
