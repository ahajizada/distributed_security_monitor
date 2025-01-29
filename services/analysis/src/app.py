from fastapi import FastAPI, HTTPException
from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from typing import Dict, Any
from datetime import datetime
import numpy as np
from sklearn.ensemble import IsolationForest
import prometheus_client
from prometheus_client import Counter, Histogram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANALYZED_LOGS = Counter('logs_analyzed_total', 'Number of logs analyzed')
DETECTED_THREATS = Counter('threats_detected_total', 'Number of threats detected')
ANALYSIS_TIME = Histogram('log_analysis_seconds', 'Time spent analyzing logs')

app = FastAPI(title="Analysis Service")

class ThreatDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
        self.feature_columns = ['timestamp', 'severity', 'source_reliability']

    def analyze_log(self, log_data: Dict[str, Any]) -> float:
        with ANALYSIS_TIME.time():
            features = self._extract_features(log_data)
            score = self.model.predict([features])[0]
            ANALYZED_LOGS.inc()
            if score == -1:
                DETECTED_THREATS.inc()
            return float(score)

    def _extract_features(self, log_data: Dict[str, Any]) -> list:
        return [
            int(datetime.fromisoformat(log_data['timestamp']).timestamp()),
            self._severity_to_numeric(log_data.get('level', 'INFO')),
            log_data.get('metadata', {}).get('source_reliability', 0.5)
        ]
    
    def _severity_to_numeric(self, severity: str) -> float:
        severity_map = {
            'DEBUG': 0.0,
            'INFO': 0.2,
            'WARNING': 0.6,
            'ERROR': 0.8,
            'CRITICAL': 1.0
        }
        return severity_map.get(severity.upper(), 0.5)

detector = ThreatDetector()

@app.post("/analyze")
async def analyze_log(log_data: Dict[str, Any]):
    try:
        threat_score = detector.analyze_log(log_data)
        return {
            "threat_score": threat_score,
            "is_threat": threat_score < 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def metrics():
    return prometheus_client.generate_latest()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
