from fastapi import HTTPException

from app.main import acknowledge_alert, app, dashboard_summary, demo_pipeline, health, ready


def test_health_and_readiness_are_distinct() -> None:
    assert health()["status"] == "healthy"
    assert ready() == {"status": "ready", "mode": "demo"}


def test_success_demo_pipeline_has_verified_health_check() -> None:
    data = demo_pipeline("success").model_dump()
    assert data["mode"] == "demo" and data["status"] == "passed"
    assert data["stages"][-1] == {"name": "health check", "status": "passed"}


def test_failure_blocks_downstream_stages() -> None:
    data = demo_pipeline("failure").model_dump()
    statuses = {stage["name"]: stage["status"] for stage in data["stages"]}
    assert statuses["test"] == "failed"
    assert statuses["build"] == statuses["deploy"] == "blocked"


def test_unknown_scenario_is_rejected() -> None:
    operation = app.openapi()["paths"]["/api/v1/pipelines/demo"]["post"]
    scenario = next(parameter for parameter in operation["parameters"] if parameter["name"] == "scenario")
    assert scenario["schema"]["enum"] == ["success", "failure"]


def test_acknowledge_alert_and_reject_unknown_alert() -> None:
    response = acknowledge_alert("ALT-284")
    assert response.model_dump() == {"id": "ALT-284", "status": "acknowledged"}
    try:
        acknowledge_alert("UNKNOWN")
    except HTTPException as error:
        assert error.status_code == 404
    else:
        raise AssertionError("unknown alert must return 404")


def test_costs_are_explicitly_simulated() -> None:
    data = dashboard_summary()
    assert data["mode"] == "demo" and data["cloud_spend_source"] == "simulated"
    assert data["cloud_spend_usd"] == 12842.60
