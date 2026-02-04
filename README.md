# Airport Security System – Collector Service

## Distributed Systems & Cloud Computing – A1

**Author:** Mustafa Fahimy  
**Semester:** Winter 2025  
**Project:** Microservices • Docker • Kubernetes • GKE Deployment

---

## Overview

This project implements the **Collector Service** for an Airport Security System composed of multiple microservices.  
The Collector acts as the **central orchestrator**, receiving image frames from cameras and forwarding them to the appropriate backend services:

- **ImageAnalysis Service** → Age & gender estimation
- **FaceRecognition Service** → Known person detection
- **Section Service** → Store demographic statistics
- **Alert Service** → Store alerts for known persons

The system is fully containerized using **Docker**, runs locally via **Docker Compose**, and is deployed to **Google Kubernetes Engine (GKE)** with autoscaling, monitoring, and ingress routing.

---

## System Architecture

Camera → Collector → ImageAnalysis → Section
↘ FaceRecognition → Alert

The Collector receives frames, forwards them to both analysis services, and handles optional `destination` forwarding.

---

## 📁 Repository Structure

```bash
a1/
├── collector/
│ ├── app.py
│ ├── requirements.txt
│ ├── Dockerfile
│ └── README.md
├── manifests/
│ ├── collector-deployment.yaml
│ ├── collector-service.yaml
│ ├── ingress.yaml
│ ├── hpa.yaml
│ └── namespace.yaml
├── docker-compose.yml
├── Project_Docs/
└── report.pdf
other descriptions
```

## Local Development (Docker Compose)

Start all services locally:

```bash
docker-compose up --build
```

Test the Collector:

```bash
curl -X POST http://localhost:8000/frame \
  -H "Content-Type: application/json" \
  -d '{"image": "<base64>"}'
```

## ☸️ Kubernetes Deployment (GKE)

1. Create cluster

```bash
gcloud container clusters create airport-cluster \
  --num-nodes=3 \
  --region=europe-west3
```

2. Deploy services

```bash
kubectl apply -f manifests/
```

3. Get external IP

```bash
kubectl get ingress
```

## Autoscaling

The Collector uses a Horizontal Pod Autoscaler:

CPU target: 70%

Min pods: 2

Max pods: 10

```bash
kubectl get hpa
```

## Monitoring

The system uses:
GKE Cloud Monitoring
Prometheus metrics
Grafana dashboards

Metrics observed:
Request latency
Pod CPU/memory usage
Autoscaling behavior
Error rates

## Note

All the details are included in the report.pf

## 📜 License

This project is for academic use only.
