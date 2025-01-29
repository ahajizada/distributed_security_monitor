# Distributed Security Monitoring System

A scalable, microservices-based security monitoring system that processes and analyzes security logs in real-time. The system provides threat detection, alerting, and visualization capabilities through a modern web dashboard and CLI tool.

## Architecture
The system consists of the following components:

- **Log Ingestion Service**: Collects and processes security logs
- **Analysis Service**: Performs real-time threat detection
- **Alert Service**: Manages and dispatches security alerts
- **Web Dashboard**: React-based visualization interface
- **CLI Tool**: Command-line interface for system interaction
- **Message Queue**: Kafka-based message broker for async communication
- **Databases**: TimescaleDB for time-series data, Elasticsearch for search

## Tech Stack

- **Backend Services**: Python (FastAPI)
- **Frontend**: React with TypeScript
- **CLI**: Python (Click)
- **Message Broker**: Apache Kafka
- **Databases**: TimescaleDB, Elasticsearch
- **Containerization**: Docker, Kubernetes
- **Monitoring**: Prometheus, Grafana

## Features

- Real-time log ingestion and processing
- ML-based threat detection
- Customizable alerting system
- Interactive dashboard with real-time visualizations
- RESTful API for system integration
- Scalable architecture using microservices
- Comprehensive monitoring and observability

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 16+
- Kubernetes cluster (for production deployment)

### Development Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/distributed-security-monitor.git
cd distributed-security-monitor
```

Start the services:

```bash
docker-compose -f docker/docker-compose.yml up
```

Access the dashboard at [http://localhost:3000](http://localhost:3000)

## Documentation

- **Architecture Overview**
- **API Documentation**
- **Development Guide**
- **Deployment Guide**
