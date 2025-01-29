import click
import requests
import json
from datetime import datetime, timedelta
from tabulate import tabulate
from typing import Dict, List

class SecurityMonitorCLI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_logs(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        response = requests.get(
            f"{self.base_url}/logs",
            params={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
        )
        response.raise_for_status()
        return response.json()

    def get_alerts(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        response = requests.get(
            f"{self.base_url}/alerts",
            params={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat()
            }
        )
        response.raise_for_status()
        return response.json()

@click.group()
def cli():
    """Security Monitoring System CLI"""
    pass

@cli.command()
@click.option('--last', default='1h', help='Time range (e.g., 1h, 24h, 7d)')
def alerts(last: str):
    """Show recent security alerts"""
    cli = SecurityMonitorCLI()
    end_time = datetime.now()
    start_time = parse_time_range(last, end_time)
    
    try:
        alerts = cli.get_alerts(start_time, end_time)
        table = [[
            a['timestamp'],
            a['severity'],
            a['message']
        ] for a in alerts]
        
        click.echo(tabulate(
            table,
            headers=['Timestamp', 'Severity', 'Message'],
            tablefmt='grid'
        ))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--last', default='1h', help='Time range (e.g., 1h, 24h, 7d)')
def logs(last: str):
    """Show recent security logs"""
    cli = SecurityMonitorCLI()
    end_time = datetime.now()
    start_time = parse_time_range(last, end_time)
    
    try:
        logs = cli.get_logs(start_time, end_time)
        table = [[
            l['timestamp'],
            l['level'],
            l['source'],
            l['message']
        ] for l in logs]
        
        click.echo(tabulate(
            table,
            headers=['Timestamp', 'Level', 'Source', 'Message'],
            tablefmt='grid'
        ))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

def parse_time_range(range_str: str, end_time: datetime) -> datetime:
    unit = range_str[-1]
    value = int(range_str[:-1])
    
    if unit == 'h':
        delta = timedelta(hours=value)
    elif unit == 'd':
        delta = timedelta(days=value)
    else:
        raise ValueError("Invalid time range format. Use 'h' for hours or 'd' for days")
    
    return end_time - delta

if __name__ == '__main__':
    cli()
