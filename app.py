"""
Streamlit UI for AI Incident Management Assistant

A beautiful, interactive dashboard for managing incidents with AI assistance.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import asyncio
from datetime import datetime
from typing import Optional

from models.schemas import Incident, Severity, IncidentStatus
from data.seed_data import (
    get_incidents, get_playbooks, get_deployments, get_alerts, SERVICES
)
from ai.vector_store import initialize_vector_store, get_vector_store
from ai.agent import IncidentAIAgent
from ai.evaluation import get_evaluation_framework


# Page config
st.set_page_config(
    page_title="AI Reliability Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .severity-critical { color: #ef4444; font-weight: bold; }
    .severity-high { color: #f97316; font-weight: bold; }
    .severity-medium { color: #eab308; font-weight: bold; }
    .severity-low { color: #22c55e; font-weight: bold; }
    .status-investigating { color: #3b82f6; }
    .status-identified { color: #f59e0b; }
    .status-monitoring { color: #8b5cf6; }
    .status-resolved { color: #22c55e; }
    .insight-card {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    .chat-user {
        background: #3b82f6;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-assistant {
        background: #f3f4f6;
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'initialized' not in st.session_state:
        # Load data
        st.session_state.incidents = get_incidents()
        st.session_state.playbooks = get_playbooks()
        st.session_state.deployments = get_deployments()
        st.session_state.alerts = get_alerts()
        st.session_state.services = SERVICES
        
        # Initialize vector store
        initialize_vector_store(
            st.session_state.incidents,
            st.session_state.playbooks,
            st.session_state.deployments,
            st.session_state.alerts
        )
        
        # Initialize AI agent
        st.session_state.agent = IncidentAIAgent(
            st.session_state.incidents,
            st.session_state.playbooks,
            st.session_state.deployments,
            st.session_state.services,
            st.session_state.alerts
        )
        
        st.session_state.selected_incident = None
        st.session_state.chat_messages = []
        st.session_state.current_insights = []
        st.session_state.initialized = True


def get_severity_color(severity: str) -> str:
    colors = {
        "critical": "#ef4444",
        "high": "#f97316",
        "medium": "#eab308",
        "low": "#22c55e"
    }
    return colors.get(severity, "#6b7280")


def get_status_color(status: str) -> str:
    colors = {
        "investigating": "#3b82f6",
        "identified": "#f59e0b",
        "monitoring": "#8b5cf6",
        "resolved": "#22c55e"
    }
    return colors.get(status, "#6b7280")


def format_time_ago(dt: datetime) -> str:
    now = datetime.now()
    diff = now - dt
    minutes = int(diff.total_seconds() / 60)
    hours = int(minutes / 60)
    days = int(hours / 24)
    
    if minutes < 60:
        return f"{minutes}m ago"
    elif hours < 24:
        return f"{hours}h ago"
    else:
        return f"{days}d ago"


def render_sidebar():
    """Render the sidebar with incident list"""
    st.sidebar.markdown("## 🛡️ **Incident AI**")
    st.sidebar.markdown("*Intelligent Response Assistant*")
    st.sidebar.markdown("---")
    
    # Filter options
    st.sidebar.markdown("### Filters")
    severity_filter = st.sidebar.multiselect(
        "Severity",
        ["critical", "high", "medium", "low"],
        default=[]
    )
    status_filter = st.sidebar.multiselect(
        "Status",
        ["investigating", "identified", "monitoring", "resolved"],
        default=[]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Incidents")
    
    # Filter incidents
    incidents = st.session_state.incidents
    if severity_filter:
        incidents = [i for i in incidents if i.severity.value in severity_filter]
    if status_filter:
        incidents = [i for i in incidents if i.status.value in status_filter]
    
    # Active incidents
    active = [i for i in incidents if i.status.value != "resolved"]
    resolved = [i for i in incidents if i.status.value == "resolved"]
    
    if active:
        st.sidebar.markdown(f"**🔴 Active ({len(active)})**")
        for inc in active:
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                if st.sidebar.button(
                    f"**{inc.severity.value.upper()}** | {inc.title[:30]}...",
                    key=f"inc-{inc.id}",
                    use_container_width=True
                ):
                    st.session_state.selected_incident = inc
                    st.session_state.chat_messages = []
                    st.session_state.current_insights = []
                    st.rerun()
    
    if resolved:
        st.sidebar.markdown(f"**✅ Resolved ({len(resolved)})**")
        for inc in resolved:
            if st.sidebar.button(
                f"{inc.title[:35]}...",
                key=f"inc-{inc.id}",
                use_container_width=True
            ):
                st.session_state.selected_incident = inc
                st.session_state.chat_messages = []
                st.session_state.current_insights = []
                st.rerun()


def render_incident_detail(incident: Incident):
    """Render incident details"""
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## {incident.title}")
    
    with col2:
        severity_color = get_severity_color(incident.severity.value)
        st.markdown(
            f'<span style="background-color: {severity_color}; color: white; '
            f'padding: 4px 12px; border-radius: 12px; font-weight: bold;">'
            f'{incident.severity.value.upper()}</span>',
            unsafe_allow_html=True
        )
    
    with col3:
        status_color = get_status_color(incident.status.value)
        st.markdown(
            f'<span style="background-color: {status_color}; color: white; '
            f'padding: 4px 12px; border-radius: 12px;">'
            f'{incident.status.value.title()}</span>',
            unsafe_allow_html=True
        )
    
    st.markdown(f"*{incident.description}*")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Started", format_time_ago(incident.created_at))
    
    with col2:
        if incident.affected_customers:
            st.metric("Affected Users", f"{incident.affected_customers:,}")
        else:
            st.metric("Affected Users", "Unknown")
    
    with col3:
        st.metric("Services", len(incident.services))
    
    with col4:
        if incident.assignee:
            st.metric("Assignee", incident.assignee.split("@")[0])
        else:
            st.metric("Assignee", "Unassigned")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Timeline", "📊 Details", "🤖 AI Insights"])
    
    with tab1:
        render_timeline(incident)
    
    with tab2:
        render_details(incident)
    
    with tab3:
        render_insights()


def render_timeline(incident: Incident):
    """Render incident timeline"""
    st.markdown("### Timeline")
    
    for event in reversed(incident.timeline):
        icon = {
            "status_change": "🔄",
            "message": "💬",
            "action": "✅",
            "ai_insight": "🤖",
            "deployment": "🚀",
            "alert": "🚨"
        }.get(event.type.value, "📌")
        
        with st.container():
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown(f"### {icon}")
            with col2:
                st.markdown(f"**{event.timestamp.strftime('%H:%M:%S')}**")
                if event.author:
                    st.markdown(f"*by {event.author}*")
                
                if event.type.value == "ai_insight":
                    st.info(event.content)
                else:
                    st.markdown(event.content)
            
            st.markdown("---")


def render_details(incident: Incident):
    """Render incident details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Services")
        for service in incident.services:
            st.markdown(f"- {service}")
        
        st.markdown("### Tags")
        tags_html = " ".join([
            f'<span style="background: #e5e7eb; padding: 2px 8px; '
            f'border-radius: 4px; margin-right: 4px;">{tag}</span>'
            for tag in incident.tags
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    with col2:
        if incident.root_cause:
            st.markdown("### Root Cause")
            st.warning(incident.root_cause)
        
        if incident.resolution:
            st.markdown("### Resolution")
            st.success(incident.resolution)
    
    if incident.slack_channel:
        st.markdown(f"**Slack:** {incident.slack_channel}")


def render_insights():
    """Render AI insights"""
    if not st.session_state.current_insights:
        st.info("Click 'Analyze with AI' to generate insights for this incident.")
        return
    
    st.markdown("### AI-Generated Insights")
    
    for insight in st.session_state.current_insights:
        confidence_pct = int(insight.confidence * 100)
        icon = "🟢" if confidence_pct > 70 else "🟡" if confidence_pct > 40 else "🟠"
        
        with st.container():
            st.markdown(
                f'<div class="insight-card">'
                f'<strong>{icon} {insight.title}</strong> '
                f'<span style="color: #6b7280;">({confidence_pct}% confidence)</span>'
                f'<br/>{insight.content}'
                f'</div>',
                unsafe_allow_html=True
            )


def render_ai_chat():
    """Render AI chat interface"""
    st.markdown("### 💬 AI Assistant")
    
    incident = st.session_state.selected_incident
    if not incident:
        st.info("Select an incident to start chatting with the AI assistant.")
        return
    
    # Quick actions
    st.markdown("**Quick Actions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_prompts = [
        ("🔍 Root Cause", "What is the likely root cause of this incident?"),
        ("🛠️ How to Fix", "How should we resolve this incident?"),
        ("📜 Similar", "Have we seen similar incidents before?"),
        ("🚀 Changes", "What recent deployments might be related?")
    ]
    
    for i, (label, prompt) in enumerate(quick_prompts):
        with [col1, col2, col3, col4][i]:
            if st.button(label, use_container_width=True):
                asyncio.run(handle_chat_message(prompt))
    
    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-assistant">{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
    
    # Chat input
    user_input = st.chat_input("Ask about this incident...")
    if user_input:
        asyncio.run(handle_chat_message(user_input))


async def handle_chat_message(message: str):
    """Handle a chat message"""
    incident = st.session_state.selected_incident
    if not incident:
        return
    
    # Add user message
    st.session_state.chat_messages.append({
        "role": "user",
        "content": message
    })
    
    # Get AI response
    agent = st.session_state.agent
    response = await agent.answer_question(incident, message)
    
    # Add assistant response
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": response.message
    })
    
    st.rerun()


async def analyze_incident():
    """Analyze the selected incident"""
    incident = st.session_state.selected_incident
    if not incident:
        return
    
    agent = st.session_state.agent
    response = await agent.analyze_incident(incident)
    
    st.session_state.current_insights = response.insights
    
    # Add analysis to chat
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": response.message
    })
    
    st.rerun()


def render_metrics_page():
    """Render the metrics dashboard"""
    st.markdown('<h1 class="main-header">AI Performance Metrics</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Evaluation framework tracking AI assistant performance</p>',
        unsafe_allow_html=True
    )
    
    eval_framework = get_evaluation_framework()
    metrics = eval_framework.get_metrics()
    stats = eval_framework.get_stats()
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Evaluations", stats.total_evaluations)
    
    with col2:
        st.metric("Avg User Rating", f"{stats.user_ratings['average']:.1f}/5")
    
    with col3:
        st.metric("P50 Latency", f"{stats.latency_percentiles['p50']:.0f}ms")
    
    with col4:
        st.metric("P99 Latency", f"{stats.latency_percentiles['p99']:.0f}ms")
    
    st.markdown("---")
    
    # Metric cards
    col1, col2 = st.columns(2)
    
    for i, metric in enumerate(metrics):
        with [col1, col2][i % 2]:
            trend_icon = "↑" if metric.trend == "up" else "↓" if metric.trend == "down" else "→"
            color = "#22c55e" if metric.value >= metric.target else "#f97316"
            
            st.markdown(f"### {metric.name}")
            st.markdown(f"*{metric.description}*")
            
            progress = min(metric.value / metric.target, 1.0) if metric.target > 0 else 0
            st.progress(progress)
            
            st.markdown(
                f'<span style="font-size: 2rem; font-weight: bold; color: {color};">'
                f'{metric.value}{metric.unit}</span> '
                f'<span style="color: #6b7280;">{trend_icon} Target: {metric.target}{metric.unit}</span>',
                unsafe_allow_html=True
            )
            st.markdown("---")
    
    # Architecture info
    st.markdown("### System Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**RAG Pipeline**")
        st.markdown("""
        - Vector embeddings for semantic search
        - Multi-source context retrieval
        - Similarity-based incident matching
        - Dynamic context window construction
        """)
        
        st.markdown("**AI Agent Capabilities**")
        st.markdown("""
        - Root cause analysis from historical patterns
        - Playbook recommendations based on incident type
        - Deployment correlation detection
        - Risk assessment and escalation suggestions
        """)
    
    with col2:
        st.markdown("**Evaluation Framework**")
        st.markdown("""
        - Automatic relevance scoring
        - User feedback collection
        - Latency tracking (P50, P90, P99)
        - Accuracy and helpfulness metrics
        """)
        
        st.markdown("**Production Considerations**")
        st.markdown("""
        - Ready for OpenAI/Claude integration
        - Pluggable vector store (Pinecone, Weaviate, Chroma)
        - Structured logging for observability
        - Rate limiting and caching strategies
        """)


def render_welcome():
    """Render welcome screen"""
    st.markdown('<h1 class="main-header">AI-Powered Incident Management</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Select an incident from the sidebar to get AI-powered insights, '
        'similar incident analysis, and intelligent recommendations.</p>',
        unsafe_allow_html=True
    )
    
    # Stats
    incidents = st.session_state.incidents
    active = [i for i in incidents if i.status.value != "resolved"]
    critical = [i for i in active if i.severity.value == "critical"]
    resolved = [i for i in incidents if i.status.value == "resolved"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            '<div class="metric-card">'
            f'<h2 style="color: #ef4444;">🚨 {len(critical)}</h2>'
            '<p>Critical Incidents</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            '<div class="metric-card">'
            f'<h2 style="color: #f97316;">⏳ {len(active)}</h2>'
            '<p>Active Incidents</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            '<div class="metric-card">'
            f'<h2 style="color: #22c55e;">✅ {len(resolved)}</h2>'
            '<p>Resolved</p>'
            '</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Quick start
    if critical:
        st.markdown("### 🚀 Quick Start")
        st.markdown("Click below to investigate the most critical incident:")
        if st.button(f"Investigate: {critical[0].title}", type="primary"):
            st.session_state.selected_incident = critical[0]
            st.rerun()


def main():
    """Main application entry point"""
    # Initialize
    init_session_state()
    
    # Sidebar
    render_sidebar()
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Dashboard", "📊 AI Metrics"],
        label_visibility="collapsed"
    )
    
    if page == "📊 AI Metrics":
        render_metrics_page()
    else:
        # Main content
        incident = st.session_state.selected_incident
        
        if incident:
            # Two column layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                render_incident_detail(incident)
            
            with col2:
                # Analyze button
                if st.button("🔮 Analyze with AI", type="primary", use_container_width=True):
                    with st.spinner("Analyzing incident..."):
                        asyncio.run(analyze_incident())
                
                render_ai_chat()
        else:
            render_welcome()


if __name__ == "__main__":
    main()
