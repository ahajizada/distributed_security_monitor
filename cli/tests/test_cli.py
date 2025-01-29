import pytest
from click.testing import CliRunner
from datetime import datetime
from security_monitor import cli, SecurityMonitorCLI

def test_alerts_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['alerts', '--last', '1h'])
    assert result.exit_code == 0

def test_logs_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['logs', '--last', '1h'])
    assert result.exit_code == 0

def test_invalid_time_range():
    runner = CliRunner()
    result = runner.invoke(cli, ['logs', '--last', '1x'])
    assert result.exit_code != 0
    assert "Invalid time range format" in result.output
