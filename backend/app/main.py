"""QlaudOps API: deterministic fixtures and clearly isolated demo simulations."""
from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Small JSON formatter for container-friendly structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"timestamp": datetime.now(UTC).isoformat(), "level": record.levelname.lower(), "logger": record.name, "message": record.getMessage()})


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), handlers=[handler], force=True)
log = logging.getLogger("qlaudops.api")

app = FastAPI(title="QlaudOps API", version="1.0.0", description="DevOps command center API. Demo endpoints simulate outcomes and never execute shell commands or contact infrastructure.")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","), allow_methods=["GET", "POST"], allow_headers=["*"])

SERVICES = [
    {"name": "api-gateway", "team": "Platform", "status": "healthy", "latency_ms": 42, "uptime": 99.98},
    {"name": "checkout-service", "team": "Commerce", "status": "degraded", "latency_ms": 238, "uptime": 99.42},
    {"name": "auth-service", "team": "Identity", "status": "healthy", "latency_ms": 31, "uptime": 99.99},
    {"name": "worker-queue", "team": "Platform", "status": "healthy", "latency_ms": 18, "uptime": 99.96},
]
ALERTS = [
    {"id": "ALT-284", "title": "Elevated latency on checkout-service", "severity": "critical", "status": "open", "age_minutes": 8},
    {"id": "ALT-283", "title": "Memory usage approaching threshold", "severity": "warning", "status": "open", "age_minutes": 14},
]


class AcknowledgeResponse(BaseModel):
    id: str
    status: Literal["acknowledged"]


class PipelineResult(BaseModel):
    mode: Literal["demo"] = "demo"
    scenario: Literal["success", "failure"]
    status: Literal["passed", "failed"]
    duration: str
    stages: list[dict[str, str]]
    message: str


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "qlaudops-api", "timestamp": datetime.now(UTC).isoformat()}


@app.get("/ready", tags=["health"])
def ready() -> dict[str, str]:
    return {"status": "ready", "mode": "demo"}


@app.get("/api/v1/dashboard/summary", tags=["dashboard"])
def dashboard_summary() -> dict:
    return {"mode": "demo", "pipeline_success_rate": 96.8, "deployments_this_month": 142, "mean_recovery_minutes": 8.4, "active_alerts": sum(a["status"] == "open" for a in ALERTS), "services": SERVICES, "cloud_spend_usd": 12842.60, "cloud_spend_source": "simulated"}


@app.get("/api/v1/services", tags=["services"])
def list_services() -> dict:
    return {"mode": "demo", "items": SERVICES}


@app.get("/api/v1/pipelines", tags=["pipelines"])
def list_pipelines() -> dict:
    return {"mode": "demo", "items": [{"id": "#1842", "name": "api-gateway · deploy", "status": "passed"}, {"id": "#1841", "name": "checkout · test", "status": "failed"}]}


@app.post("/api/v1/pipelines/demo", response_model=PipelineResult, tags=["pipelines"])
def demo_pipeline(scenario: Literal["success", "failure"] = "success") -> PipelineResult:
    """Return a deterministic pipeline simulation. This route never runs build tools."""
    if scenario == "failure":
        result = PipelineResult(scenario=scenario, status="failed", duration="48s", stages=[{"name": "validate", "status": "passed"}, {"name": "test", "status": "failed"}, {"name": "build", "status": "blocked"}, {"name": "deploy", "status": "blocked"}], message="Intentional demo assertion failure. Build and deployment were blocked.")
    else:
        result = PipelineResult(scenario=scenario, status="passed", duration="1m 08s", stages=[{"name": "validate", "status": "passed"}, {"name": "test", "status": "passed"}, {"name": "build", "status": "simulated"}, {"name": "manifest validation", "status": "simulated"}, {"name": "deploy", "status": "simulated"}, {"name": "health check", "status": "passed"}], message="Demo checks passed. Deployment stages are simulated; application health endpoint verified.")
    log.info("demo pipeline completed scenario=%s status=%s", result.scenario, result.status)
    return result


@app.get("/api/v1/alerts", tags=["alerts"])
def list_alerts() -> dict:
    return {"mode": "demo", "items": ALERTS}


@app.post("/api/v1/alerts/{alert_id}/acknowledge", response_model=AcknowledgeResponse, tags=["alerts"])
def acknowledge_alert(alert_id: str) -> AcknowledgeResponse:
    alert = next((item for item in ALERTS if item["id"] == alert_id), None)
    if alert is None:
        raise HTTPException(status_code=404, detail={"code": "alert_not_found", "message": "No matching demo alert exists."})
    alert["status"] = "acknowledged"
    log.info("demo alert acknowledged id=%s", alert_id)
    return AcknowledgeResponse(id=alert_id, status="acknowledged")


@app.post("/api/v1/demo/recover", tags=["demo"])
def demo_recovery() -> dict[str, str]:
    log.info("simulated recovery verified service=checkout-service")
    return {"mode": "demo", "service": "checkout-service", "status": "recovered", "health_check": "passed", "message": "Simulated recovery only; no cluster was modified."}


@app.get("/api/v1/deployments", tags=["deployments"])
def list_deployments() -> dict:
    return {"mode": "demo", "items": [{"service": "api-gateway", "version": "v2.4.2", "environment": "Production", "status": "healthy"}, {"service": "auth-service", "version": "v1.18.0", "environment": "Production", "status": "healthy"}]}


@app.get("/api/v1/costs", tags=["costs"])
def costs() -> dict:
    return {"mode": "demo", "currency": "USD", "total": 12842.60, "source": "simulated", "items": [{"service": "Amazon EKS", "amount": 6240.00}, {"service": "Amazon EC2", "amount": 3810.50}]}


@app.get("/api/v1/backups", tags=["backups"])
def backups() -> dict:
    return {"mode": "demo", "items": [{"resource": "Kubernetes manifests", "status": "version_controlled", "recovery_tested": True}, {"resource": "Database snapshots", "status": "not_configured", "recovery_tested": False}]}


@app.get("/api/v1/integrations/status", tags=["integrations"])
def integrations_status() -> dict:
    return {"mode": "demo", "items": [{"name": "GitHub Actions", "status": "example_workflow_configured", "credentials_configured": False}, {"name": "Amazon EKS", "status": "not_configured", "credentials_configured": False}, {"name": "Prometheus", "status": "demo_only", "credentials_configured": False}]}


static_dir = Path(__file__).resolve().parents[1] / "static"
Instrumentator().instrument(app).expose(app)
if static_dir.is_dir():
    from fastapi.staticfiles import StaticFiles

    app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
