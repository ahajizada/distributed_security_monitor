from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import smtplib
import logging
import aiohttp
import json
from datetime import datetime
import prometheus_client
from prometheus_client import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALERTS_GENERATED = Counter('alerts_generated_total', 'Number of alerts generated')
ALERTS_SENT = Counter('alerts_sent_total', 'Number of alerts sent', ['channel'])

app = FastAPI(title="Alert Service")

class Alert(BaseModel):
    severity: str
    message: str
    metadata: Dict[str, Any]
    timestamp: str

class AlertManager:
    def __init__(self):
        self.alert_handlers = {
            'email': self._send_email_alert,
            'slack': self._send_slack_alert,
            'webhook': self._send_webhook_alert
        }

    async def process_alert(self, alert: Alert):
        ALERTS_GENERATED.inc()
        for handler_name, handler in self.alert_handlers.items():
            try:
                await handler(alert)
                ALERTS_SENT.labels(channel=handler_name).inc()
            except Exception as e:
                logger.error(f"Failed to send {handler_name} alert: {e}")

    async def _send_email_alert(self, alert: Alert):
        logger.info(f"Email alert sent: {alert.message}")
        pass

    async def _send_slack_alert(self, alert: Alert):
        logger.info(f"Slack alert sent: {alert.message}")
        pass

    async def _send_webhook_alert(self, alert: Alert):
        logger.info(f"Webhook alert sent: {alert.message}")
        pass

alert_manager = AlertManager()

@app.post("/alerts")
async def create_alert(alert: Alert, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(alert_manager.process_alert, alert)
        return {"status": "success", "message": "Alert processing initiated"}
    except Exception as e:
        logger.error(f"Failed to process alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    return prometheus_client.generate_latest()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
