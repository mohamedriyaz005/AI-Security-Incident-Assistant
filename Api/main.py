"""
FastAPI Backend for AI Incident Management Assistant

Provides REST API endpoints for:
- Incident analysis
- AI chat
- Vector search
- Evaluation metrics
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models.schemas import (
    AnalyzeRequest, ChatRequest, SearchRequest, FeedbackRequest,
    Incident, AIInsight
)
from data.seed_data import (
    get_incidents, get_playbooks, get_deployments, get_alerts, SERVICES
)
from ai.vector_store import initialize_vector_store, get_vector_store
from ai.agent import IncidentAIAgent
from ai.evaluation import get_evaluation_framework


# Global state
incidents_db = {}
agent: Optional[IncidentAIAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize data on startup"""
    global incidents_db, agent
    
    # Load seed data
    incidents = get_incidents()
    playbooks = get_playbooks()
    deployments = get_deployments()
    alerts = get_alerts()
    
    # Build incident lookup
    incidents_db = {inc.id: inc for inc in incidents}
    
    # Initialize vector store
    initialize_vector_store(incidents, playbooks, deployments, alerts)
    
    # Initialize AI agent
    agent = IncidentAIAgent(incidents, playbooks, deployments, SERVICES, alerts)
    
    print("✅ API initialized with seed data")
    print(f"   - {len(incidents)} incidents")
    print(f"   - {len(playbooks)} playbooks")
    print(f"   - {len(deployments)} deployments")
    print(f"   - {len(alerts)} alerts")
    
    yield
    
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Incident Management Assistant",
    description="RAG-powered AI assistant for incident response",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class AnalyzeResponse(BaseModel):
    success: bool
    message: str
    insights: List[dict]
    suggested_actions: List[str]
    confidence: float


class ChatResponse(BaseModel):
    success: bool
    message: str
    insights: List[dict]
    confidence: float
    evaluation_id: Optional[str] = None


class SearchResponse(BaseModel):
    success: bool
    results: List[dict]
    total: int
    stats: dict


class MetricsResponse(BaseModel):
    success: bool
    metrics: List[dict]
    stats: dict


class IncidentListResponse(BaseModel):
    success: bool
    incidents: List[dict]
    total: int


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Incident Management Assistant",
        "version": "1.0.0"
    }


@app.get("/api/incidents", response_model=IncidentListResponse)
async def list_incidents():
    """Get all incidents"""
    incidents = list(incidents_db.values())
    return IncidentListResponse(
        success=True,
        incidents=[inc.model_dump() for inc in incidents],
        total=len(incidents)
    )


@app.get("/api/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """Get a specific incident"""
    if incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return {
        "success": True,
        "incident": incidents_db[incident_id].model_dump()
    }


@app.post("/api/ai/analyze", response_model=AnalyzeResponse)
async def analyze_incident(request: AnalyzeRequest):
    """
    Analyze an incident using the AI agent.
    
    Returns insights, recommendations, and context from RAG.
    """
    if request.incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident = incidents_db[request.incident_id]
    
    try:
        response = await agent.analyze_incident(incident)
        
        # Record for evaluation
        eval_framework = get_evaluation_framework()
        eval_framework.record_response(
            incident_id=request.incident_id,
            response_id=f"resp-{datetime.now().timestamp()}",
            start_time=datetime.now(),
            response=response.message,
            context=response.context
        )
        
        return AnalyzeResponse(
            success=True,
            message=response.message,
            insights=[insight.model_dump() for insight in response.insights],
            suggested_actions=response.suggested_actions,
            confidence=response.confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat with the AI about an incident.
    
    Supports questions about root cause, resolution, similar incidents, etc.
    """
    if request.incident_id not in incidents_db:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident = incidents_db[request.incident_id]
    start_time = datetime.now()
    
    try:
        response = await agent.answer_question(incident, request.message)
        
        # Record for evaluation
        eval_framework = get_evaluation_framework()
        evaluation_id = eval_framework.record_response(
            incident_id=request.incident_id,
            response_id=f"resp-{datetime.now().timestamp()}",
            start_time=start_time,
            response=response.message,
            context=response.context
        )
        
        return ChatResponse(
            success=True,
            message=response.message,
            insights=[insight.model_dump() for insight in response.insights],
            confidence=response.confidence,
            evaluation_id=evaluation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai/search", response_model=SearchResponse)
async def search_knowledge(request: SearchRequest):
    """
    Search the knowledge base using vector similarity.
    
    Returns relevant incidents, playbooks, deployments, and alerts.
    """
    try:
        vector_store = get_vector_store()
        results = vector_store.search(
            query=request.query,
            limit=request.limit,
            doc_types=request.types
        )
        
        return SearchResponse(
            success=True,
            results=[
                {
                    "id": r.document.id,
                    "title": r.document.metadata.get("title", "Unknown"),
                    "type": r.document.metadata.get("type", "unknown"),
                    "score": r.score,
                    "highlights": r.highlights
                }
                for r in results
            ],
            total=len(results),
            stats=vector_store.get_stats()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get AI evaluation metrics.
    
    Returns relevance, accuracy, helpfulness, and latency metrics.
    """
    try:
        eval_framework = get_evaluation_framework()
        metrics = eval_framework.get_metrics()
        stats = eval_framework.get_stats()
        
        return MetricsResponse(
            success=True,
            metrics=[
                {
                    "id": m.id,
                    "name": m.name,
                    "description": m.description,
                    "value": m.value,
                    "target": m.target,
                    "unit": m.unit,
                    "trend": m.trend,
                    "history": [{"date": h.date, "value": h.value} for h in m.history]
                }
                for m in metrics
            ],
            stats={
                "total_evaluations": stats.total_evaluations,
                "average_scores": stats.average_scores,
                "user_ratings": stats.user_ratings,
                "latency_percentiles": stats.latency_percentiles
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for an AI response"""
    try:
        eval_framework = get_evaluation_framework()
        eval_framework.record_feedback(
            evaluation_id=request.evaluation_id,
            rating=request.rating,
            helpful=request.helpful,
            comment=request.comment
        )
        
        return {"success": True, "message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
