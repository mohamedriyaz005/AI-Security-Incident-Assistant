"""
Pydantic models for the AI Incident Management System
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentStatus(str, Enum):
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"


class TimelineEventType(str, Enum):
    STATUS_CHANGE = "status_change"
    MESSAGE = "message"
    ACTION = "action"
    AI_INSIGHT = "ai_insight"
    DEPLOYMENT = "deployment"
    ALERT = "alert"


class TimelineEvent(BaseModel):
    id: str
    timestamp: datetime
    type: TimelineEventType
    content: str
    author: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Incident(BaseModel):
    id: str
    title: str
    description: str
    severity: Severity
    status: IncidentStatus
    services: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    assignee: Optional[str] = None
    commander: Optional[str] = None
    timeline: List[TimelineEvent] = []
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    customer_impact: Optional[str] = None
    affected_customers: Optional[int] = None
    slack_channel: Optional[str] = None
    jira_ticket: Optional[str] = None


class PlaybookStep(BaseModel):
    id: str
    order: int
    title: str
    description: str
    commands: List[str] = []
    links: List[str] = []
    is_automated: bool = False


class Playbook(BaseModel):
    id: str
    title: str
    description: str
    services: List[str]
    severity: List[Severity]
    steps: List[PlaybookStep]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0
    avg_resolution_time: Optional[int] = None  # minutes


class DeploymentStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    IN_PROGRESS = "in_progress"


class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


class Deployment(BaseModel):
    id: str
    service: str
    version: str
    environment: Environment
    status: DeploymentStatus
    deployed_at: datetime
    deployed_by: str
    commit_sha: str
    commit_message: str
    changed_files: List[str]
    rollback_available: bool = True


class ServiceStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"


class Service(BaseModel):
    id: str
    name: str
    description: str
    owner: str
    team: str
    repository: str
    status: ServiceStatus
    dependencies: List[str]
    oncall_rotation: List[str]
    slack_channel: Optional[str] = None
    dashboard_url: Optional[str] = None


class AlertStatus(str, Enum):
    FIRING = "firing"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Alert(BaseModel):
    id: str
    title: str
    description: str
    severity: Severity
    source: str
    service: str
    status: AlertStatus
    fired_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    related_incident_id: Optional[str] = None


# AI-specific models

class InsightType(str, Enum):
    ROOT_CAUSE = "root_cause"
    RECOMMENDATION = "recommendation"
    SIMILAR_PATTERN = "similar_pattern"
    RISK_ASSESSMENT = "risk_assessment"


class AIInsight(BaseModel):
    id: str
    type: InsightType
    title: str
    content: str
    confidence: float = Field(ge=0, le=1)
    sources: List[str] = []
    created_at: datetime


class SimilarIncident(BaseModel):
    incident: Incident
    similarity: float = Field(ge=0, le=1)
    matched_on: List[str]


class AIContext(BaseModel):
    incident: Incident
    similar_incidents: List[SimilarIncident]
    relevant_playbooks: List[Playbook]
    recent_deployments: List[Deployment]
    related_alerts: List[Alert]
    service_info: List[Service]


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class AIMessage(BaseModel):
    id: str
    role: MessageRole
    content: str
    timestamp: datetime
    context: Optional[AIContext] = None
    insights: Optional[List[AIInsight]] = None


class ChatSession(BaseModel):
    id: str
    incident_id: str
    messages: List[AIMessage] = []
    created_at: datetime
    updated_at: datetime


# Evaluation models

class EvaluationMetrics(BaseModel):
    relevance: float = Field(ge=0, le=1)
    accuracy: float = Field(ge=0, le=1)
    helpfulness: float = Field(ge=0, le=1)
    latency_ms: float


class AIEvaluation(BaseModel):
    id: str
    incident_id: str
    response_id: str
    metrics: EvaluationMetrics
    feedback: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    evaluated_at: datetime
    evaluated_by: Optional[str] = None


# API request/response models

class AnalyzeRequest(BaseModel):
    incident_id: str


class ChatRequest(BaseModel):
    incident_id: str
    message: str


class SearchRequest(BaseModel):
    query: str
    types: Optional[List[str]] = None
    limit: int = 10


class AgentResponse(BaseModel):
    message: str
    insights: List[AIInsight]
    suggested_actions: List[str]
    context: AIContext
    confidence: float


class FeedbackRequest(BaseModel):
    evaluation_id: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    helpful: bool
    comment: Optional[str] = None
