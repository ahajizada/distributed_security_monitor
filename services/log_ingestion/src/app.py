from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer
import uvicorn
import json
import logging
from datetime import datetime
from typing import Dict, Any
import prometheus_client
from prometheus_client import Counter, Histogram

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize metrics
INGESTED_LOGS = Counter('logs_ingested_total', 'Number of logs ingested')
LOG_PROCESSING_TIME = Histogram('log_processing_seconds', 'Time spent processing logs')

app = FastAPI(title="Log Ingestion Service")

class LogEntry(BaseModel):
    source: str
    timestamp: datetime
    level: str
    message: str
    metadata: Dict[str, Any]

class KafkaConfig:
    BOOTSTRAP_SERVERS = ['kafka:9092']
    TOPIC = 'security-logs'

try:
    producer = KafkaProducer(
        bootstrap_servers=KafkaConfig.BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
    )
except Exception as e:
    logger.error(f"Failed to initialize Kafka producer: {e}")
    raise

@app.post("/logs")
async def ingest_log(log_entry: LogEntry):
    try:
        with LOG_PROCESSING_TIME.time():
            enriched_log = {
                **log_entry.dict(),
                'processed_at': datetime.utcnow().isoformat(),
                'service': 'log-ingestion'
            }
            
            future = producer.send(
                KafkaConfig.TOPIC,
                value=enriched_log
            )
            future.get(timeout=10)
            
            INGESTED_LOGS.inc()
            
            logger.info(f"Log ingested successfully: {log_entry.source}")
            return {"status": "success", "message": "Log ingested successfully"}
    
    except Exception as e:
        logger.error(f"Failed to ingest log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    return prometheus_client.generate_latest()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
