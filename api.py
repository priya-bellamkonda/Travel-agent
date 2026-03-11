""" api.py — FastAPI entry point for the Travel Planner.Exposes a single POST /plan endpoint consumed by the frontend and a GET /health endpoint for Cloud Run health checks."""

import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from dotenv import dotenv_values
_env_path = os.path.join(ROOT, ".env")
if os.path.exists(_env_path):
    for _k, _v in dotenv_values(_env_path).items():
        os.environ[_k] = _v

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from graph import build_graph
from skills.security_skill import validate_city, llmguard_status, audit_log

app = FastAPI(
    title="Weather-Aware Travel Planner API",
    description="Multi-agent travel planning powered by LangGraph + LLM Guard",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlanRequest(BaseModel):
    city: str


class PlanResponse(BaseModel):
    city: str
    weather_report: str
    packing_advice: str
    activity_suggestions: str
    restaurant_suggestions: str
    final_summary: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm_guard": llmguard_status(),
    }


@app.post("/plan", response_model=PlanResponse)
def plan_trip(request: PlanRequest):
    # Security: validate city input before touching any agent 
    valid, result = validate_city(request.city)
    if not valid:
        audit_log("API", "BLOCKED", f"city='{request.city}' reason={result}")
        raise HTTPException(status_code=400, detail=result)

    city = result
    audit_log("API", "REQUEST", f"city={city}")

    try:
        graph = build_graph()
        state = graph.invoke({
            "city": city,
            "weather_report": "",
            "packing_advice": "",
            "activity_suggestions": "",
            "restaurant_suggestions": "",
            "final_summary": "",
            "_signature": "",
        })
    except Exception as e:
        audit_log("API", "ERROR", str(e))
        raise HTTPException(status_code=500, detail=f"Agent pipeline failed: {str(e)}")

    audit_log("API", "RESPONSE", f"city={city}")
    return PlanResponse(
        city=city,
        weather_report=state["weather_report"],
        packing_advice=state["packing_advice"],
        activity_suggestions=state["activity_suggestions"],
        restaurant_suggestions=state["restaurant_suggestions"],
        final_summary=state["final_summary"],
    )


# Serve frontend 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

_static = os.path.join(ROOT, "static")
if os.path.exists(_static):
    app.mount("/static", StaticFiles(directory=_static), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(ROOT, "static", "index.html"))