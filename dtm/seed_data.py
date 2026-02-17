"""
Sample data for the AI Incident Management System
"""

from datetime import datetime, timedelta
from models.schemas import (
    Incident, Playbook, Deployment, Service, Alert,
    TimelineEvent, PlaybookStep,
    Severity, IncidentStatus, TimelineEventType,
    DeploymentStatus, Environment, ServiceStatus, AlertStatus
)


def get_current_time():
    return datetime.now()


def hours_ago(hours: int) -> datetime:
    return get_current_time() - timedelta(hours=hours)


def minutes_ago(minutes: int) -> datetime:
    return get_current_time() - timedelta(minutes=minutes)


def days_ago(days: int) -> datetime:
    return get_current_time() - timedelta(days=days)


# Services
SERVICES = [
    Service(
        id="svc-1",
        name="API Gateway",
        description="Main API gateway handling all incoming requests",
        owner="Platform Team",
        team="platform",
        repository="github.com/company/api-gateway",
        status=ServiceStatus.HEALTHY,
        dependencies=["auth-service", "rate-limiter"],
        oncall_rotation=["alice@company.com", "bob@company.com"],
        slack_channel="#api-gateway-alerts",
        dashboard_url="https://grafana.company.com/d/api-gateway"
    ),
    Service(
        id="svc-2",
        name="Payment Service",
        description="Handles all payment processing and transactions",
        owner="Payments Team",
        team="payments",
        repository="github.com/company/payment-service",
        status=ServiceStatus.HEALTHY,
        dependencies=["database", "stripe-integration", "audit-service"],
        oncall_rotation=["charlie@company.com", "diana@company.com"],
        slack_channel="#payments-alerts",
        dashboard_url="https://grafana.company.com/d/payments"
    ),
    Service(
        id="svc-3",
        name="User Service",
        description="User authentication and profile management",
        owner="Identity Team",
        team="identity",
        repository="github.com/company/user-service",
        status=ServiceStatus.HEALTHY,
        dependencies=["database", "redis-cache", "email-service"],
        oncall_rotation=["eve@company.com", "frank@company.com"],
        slack_channel="#identity-alerts",
        dashboard_url="https://grafana.company.com/d/user-service"
    ),
    Service(
        id="svc-4",
        name="Database Cluster",
        description="Primary PostgreSQL database cluster",
        owner="Infrastructure Team",
        team="infrastructure",
        repository="github.com/company/db-config",
        status=ServiceStatus.HEALTHY,
        dependencies=[],
        oncall_rotation=["george@company.com", "helen@company.com"],
        slack_channel="#database-alerts",
        dashboard_url="https://grafana.company.com/d/database"
    ),
    Service(
        id="svc-5",
        name="Search Service",
        description="Elasticsearch-powered search functionality",
        owner="Search Team",
        team="search",
        repository="github.com/company/search-service",
        status=ServiceStatus.DEGRADED,
        dependencies=["elasticsearch", "api-gateway"],
        oncall_rotation=["ivan@company.com", "julia@company.com"],
        slack_channel="#search-alerts",
        dashboard_url="https://grafana.company.com/d/search"
    )
]


def get_incidents() -> list[Incident]:
    """Generate incidents with current timestamps"""
    return [
        Incident(
            id="inc-001",
            title="Payment Processing Failures - Stripe Integration",
            description="Multiple customers reporting failed payment transactions. Error rate spiked from 0.1% to 15% in the last 30 minutes.",
            severity=Severity.CRITICAL,
            status=IncidentStatus.INVESTIGATING,
            services=["Payment Service", "API Gateway"],
            tags=["payments", "stripe", "customer-facing"],
            created_at=minutes_ago(45),
            updated_at=minutes_ago(5),
            assignee="charlie@company.com",
            commander="diana@company.com",
            customer_impact="Customers unable to complete purchases",
            affected_customers=2500,
            slack_channel="#inc-payment-failures",
            timeline=[
                TimelineEvent(
                    id="evt-1",
                    timestamp=minutes_ago(45),
                    type=TimelineEventType.ALERT,
                    content="PagerDuty alert triggered: Payment error rate exceeded threshold (15%)",
                    metadata={"alertId": "alert-123", "source": "datadog"}
                ),
                TimelineEvent(
                    id="evt-2",
                    timestamp=minutes_ago(40),
                    type=TimelineEventType.STATUS_CHANGE,
                    content="Incident created and status set to Investigating",
                    author="diana@company.com"
                ),
                TimelineEvent(
                    id="evt-3",
                    timestamp=minutes_ago(35),
                    type=TimelineEventType.MESSAGE,
                    content="Checking Stripe dashboard for any ongoing issues on their end",
                    author="charlie@company.com"
                ),
                TimelineEvent(
                    id="evt-4",
                    timestamp=minutes_ago(30),
                    type=TimelineEventType.DEPLOYMENT,
                    content="Recent deployment detected: payment-service v2.3.4 deployed 2 hours ago",
                    metadata={"deploymentId": "dep-456", "version": "2.3.4"}
                ),
                TimelineEvent(
                    id="evt-5",
                    timestamp=minutes_ago(25),
                    type=TimelineEventType.AI_INSIGHT,
                    content="AI Analysis: Similar incident occurred on 2024-01-15. Root cause was misconfigured Stripe webhook endpoint after deployment. Recommend checking webhook configuration.",
                    metadata={"confidence": 0.87, "similarIncidentId": "inc-old-001"}
                )
            ]
        ),
        Incident(
            id="inc-002",
            title="Database Connection Pool Exhaustion",
            description="PostgreSQL connection pool maxed out causing timeouts across multiple services. Active connections at 100% capacity.",
            severity=Severity.HIGH,
            status=IncidentStatus.IDENTIFIED,
            services=["Database Cluster", "User Service", "Payment Service"],
            tags=["database", "performance", "connection-pool"],
            created_at=hours_ago(2),
            updated_at=minutes_ago(30),
            assignee="george@company.com",
            commander="helen@company.com",
            customer_impact="Intermittent slow page loads and timeouts",
            affected_customers=15000,
            slack_channel="#inc-db-connections",
            root_cause="Memory leak in User Service causing connections not being released properly",
            timeline=[
                TimelineEvent(
                    id="evt-6",
                    timestamp=hours_ago(2),
                    type=TimelineEventType.ALERT,
                    content="Alert: Database connection pool at 95% capacity",
                    metadata={"alertId": "alert-456"}
                ),
                TimelineEvent(
                    id="evt-7",
                    timestamp=hours_ago(1) + timedelta(minutes=30),
                    type=TimelineEventType.STATUS_CHANGE,
                    content="Status changed to Identified - Root cause found in User Service",
                    author="george@company.com"
                ),
                TimelineEvent(
                    id="evt-8",
                    timestamp=hours_ago(1),
                    type=TimelineEventType.ACTION,
                    content="Temporarily increased connection pool size from 100 to 150",
                    author="helen@company.com"
                )
            ]
        ),
        Incident(
            id="inc-003",
            title="Search Service Latency Degradation",
            description="Search queries taking 5-10x longer than normal. P99 latency increased from 200ms to 2s.",
            severity=Severity.MEDIUM,
            status=IncidentStatus.MONITORING,
            services=["Search Service"],
            tags=["search", "latency", "elasticsearch"],
            created_at=hours_ago(4),
            updated_at=hours_ago(1),
            assignee="ivan@company.com",
            commander="julia@company.com",
            customer_impact="Slow search results for users",
            affected_customers=5000,
            slack_channel="#inc-search-latency",
            root_cause="Elasticsearch index fragmentation after large data migration",
            timeline=[
                TimelineEvent(
                    id="evt-9",
                    timestamp=hours_ago(4),
                    type=TimelineEventType.ALERT,
                    content="Search latency P99 exceeded 1s threshold",
                    metadata={"alertId": "alert-789"}
                ),
                TimelineEvent(
                    id="evt-10",
                    timestamp=hours_ago(3),
                    type=TimelineEventType.MESSAGE,
                    content="Started force merge on fragmented indices",
                    author="ivan@company.com"
                ),
                TimelineEvent(
                    id="evt-11",
                    timestamp=hours_ago(1),
                    type=TimelineEventType.STATUS_CHANGE,
                    content="Status changed to Monitoring - Force merge completed, observing results",
                    author="ivan@company.com"
                )
            ]
        ),
        Incident(
            id="inc-004",
            title="API Rate Limiting Incorrectly Applied",
            description="Premium customers being rate limited incorrectly. Rate limiter not recognizing premium tier.",
            severity=Severity.HIGH,
            status=IncidentStatus.RESOLVED,
            services=["API Gateway"],
            tags=["rate-limiting", "customer-tiers", "configuration"],
            created_at=days_ago(1),
            updated_at=hours_ago(20),
            resolved_at=hours_ago(20),
            assignee="alice@company.com",
            commander="bob@company.com",
            customer_impact="Premium customers experiencing 429 errors",
            affected_customers=500,
            slack_channel="#inc-rate-limiting",
            root_cause="Configuration drift after infrastructure update - rate limit rules not applied to new gateway instances",
            resolution="Updated Terraform configuration and re-applied rate limit rules to all gateway instances",
            timeline=[
                TimelineEvent(
                    id="evt-12",
                    timestamp=days_ago(1),
                    type=TimelineEventType.ALERT,
                    content="Customer support tickets spiking - premium users reporting 429 errors",
                    metadata={"alertId": "alert-321"}
                ),
                TimelineEvent(
                    id="evt-13",
                    timestamp=hours_ago(23),
                    type=TimelineEventType.MESSAGE,
                    content="Identified: New gateway instances missing rate limit configuration",
                    author="alice@company.com"
                ),
                TimelineEvent(
                    id="evt-14",
                    timestamp=hours_ago(21),
                    type=TimelineEventType.ACTION,
                    content="Applied hotfix: Rate limit rules pushed to all instances",
                    author="bob@company.com"
                ),
                TimelineEvent(
                    id="evt-15",
                    timestamp=hours_ago(20),
                    type=TimelineEventType.STATUS_CHANGE,
                    content="Incident resolved - All premium customers have correct rate limits",
                    author="bob@company.com"
                )
            ]
        ),
        Incident(
            id="inc-005",
            title="Memory Leak in User Service Container",
            description="User service pods restarting every 2-3 hours due to OOMKilled. Memory usage growing linearly.",
            severity=Severity.MEDIUM,
            status=IncidentStatus.RESOLVED,
            services=["User Service"],
            tags=["memory-leak", "kubernetes", "performance"],
            created_at=days_ago(3),
            updated_at=days_ago(2),
            resolved_at=days_ago(2),
            assignee="eve@company.com",
            commander="frank@company.com",
            customer_impact="Brief authentication failures during pod restarts",
            affected_customers=1000,
            slack_channel="#inc-user-service-memory",
            root_cause="Unbounded cache growth in session validation middleware",
            resolution="Implemented LRU cache with 10,000 entry limit and TTL of 1 hour",
            timeline=[
                TimelineEvent(
                    id="evt-16",
                    timestamp=days_ago(3),
                    type=TimelineEventType.ALERT,
                    content="Multiple OOMKilled events for user-service pods",
                    metadata={"alertId": "alert-654"}
                ),
                TimelineEvent(
                    id="evt-17",
                    timestamp=days_ago(2) + timedelta(hours=12),
                    type=TimelineEventType.MESSAGE,
                    content="Heap dump analysis shows session cache growing unbounded",
                    author="eve@company.com"
                ),
                TimelineEvent(
                    id="evt-18",
                    timestamp=days_ago(2),
                    type=TimelineEventType.ACTION,
                    content="Deployed fix with LRU cache implementation",
                    author="eve@company.com"
                )
            ]
        )
    ]


def get_playbooks() -> list[Playbook]:
    """Get sample playbooks"""
    return [
        Playbook(
            id="pb-001",
            title="Payment Processing Failure Response",
            description="Standard operating procedure for investigating and resolving payment processing failures",
            services=["Payment Service"],
            severity=[Severity.CRITICAL, Severity.HIGH],
            tags=["payments", "stripe", "transactions"],
            created_at=datetime(2024, 1, 1),
            updated_at=datetime(2024, 2, 15),
            usage_count=23,
            avg_resolution_time=45,
            steps=[
                PlaybookStep(
                    id="step-1",
                    order=1,
                    title="Check Stripe Status",
                    description="Verify if there are any ongoing issues on Stripe's end",
                    commands=[],
                    links=["https://status.stripe.com", "https://dashboard.stripe.com/logs"],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-2",
                    order=2,
                    title="Review Recent Deployments",
                    description="Check if any recent deployments to payment service might have caused the issue",
                    commands=["kubectl rollout history deployment/payment-service -n production"],
                    links=["https://github.com/company/payment-service/releases"],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-3",
                    order=3,
                    title="Check Webhook Configuration",
                    description="Verify Stripe webhook endpoints are correctly configured and receiving events",
                    commands=['curl -X GET https://api.stripe.com/v1/webhook_endpoints -H "Authorization: Bearer $STRIPE_KEY"'],
                    links=["https://dashboard.stripe.com/webhooks"],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-4",
                    order=4,
                    title="Review Error Logs",
                    description="Analyze payment service error logs for patterns",
                    commands=["kubectl logs -l app=payment-service -n production --since=1h | grep -i error"],
                    links=["https://grafana.company.com/d/payment-errors"],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-5",
                    order=5,
                    title="Rollback if Needed",
                    description="If a recent deployment caused the issue, initiate rollback",
                    commands=["kubectl rollout undo deployment/payment-service -n production"],
                    links=[],
                    is_automated=False
                )
            ]
        ),
        Playbook(
            id="pb-002",
            title="Database Connection Pool Exhaustion",
            description="Steps to diagnose and resolve database connection pool exhaustion issues",
            services=["Database Cluster"],
            severity=[Severity.CRITICAL, Severity.HIGH],
            tags=["database", "postgresql", "connections"],
            created_at=datetime(2024, 1, 15),
            updated_at=datetime(2024, 2, 20),
            usage_count=15,
            avg_resolution_time=60,
            steps=[
                PlaybookStep(
                    id="step-6",
                    order=1,
                    title="Check Connection Stats",
                    description="Get current connection pool statistics",
                    commands=[
                        "SELECT count(*) FROM pg_stat_activity;",
                        "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"
                    ],
                    links=["https://grafana.company.com/d/postgres-connections"],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-7",
                    order=2,
                    title="Identify Connection Hogs",
                    description="Find services/queries holding the most connections",
                    commands=[
                        "SELECT application_name, count(*) FROM pg_stat_activity GROUP BY application_name ORDER BY count DESC;"
                    ],
                    links=[],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-8",
                    order=3,
                    title="Kill Idle Connections",
                    description="Terminate idle connections that have been open too long",
                    commands=[
                        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle' AND query_start < now() - interval '10 minutes';"
                    ],
                    links=[],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-9",
                    order=4,
                    title="Scale Connection Pool",
                    description="Temporarily increase max connections if needed",
                    commands=["ALTER SYSTEM SET max_connections = 200;", "SELECT pg_reload_conf();"],
                    links=[],
                    is_automated=False
                )
            ]
        ),
        Playbook(
            id="pb-003",
            title="Elasticsearch Latency Investigation",
            description="Diagnose and resolve high latency issues in Elasticsearch",
            services=["Search Service"],
            severity=[Severity.MEDIUM, Severity.HIGH],
            tags=["elasticsearch", "search", "latency"],
            created_at=datetime(2024, 2, 1),
            updated_at=datetime(2024, 2, 25),
            usage_count=8,
            avg_resolution_time=90,
            steps=[
                PlaybookStep(
                    id="step-10",
                    order=1,
                    title="Check Cluster Health",
                    description="Verify Elasticsearch cluster health status",
                    commands=['curl -X GET "localhost:9200/_cluster/health?pretty"'],
                    links=["https://kibana.company.com/app/monitoring"],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-11",
                    order=2,
                    title="Review Index Stats",
                    description="Check for index fragmentation and segment counts",
                    commands=['curl -X GET "localhost:9200/_cat/indices?v&s=store.size:desc"'],
                    links=[],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-12",
                    order=3,
                    title="Force Merge Indices",
                    description="Run force merge to reduce segment count",
                    commands=['curl -X POST "localhost:9200/_forcemerge?max_num_segments=1"'],
                    links=[],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-13",
                    order=4,
                    title="Clear Field Data Cache",
                    description="Clear field data cache if memory is high",
                    commands=['curl -X POST "localhost:9200/_cache/clear?fielddata=true"'],
                    links=[],
                    is_automated=False
                )
            ]
        ),
        Playbook(
            id="pb-004",
            title="Memory Leak Investigation",
            description="Steps to identify and fix memory leaks in containerized services",
            services=["User Service", "Payment Service", "API Gateway"],
            severity=[Severity.MEDIUM, Severity.HIGH],
            tags=["memory", "leak", "kubernetes", "debugging"],
            created_at=datetime(2024, 1, 20),
            updated_at=datetime(2024, 2, 10),
            usage_count=12,
            avg_resolution_time=120,
            steps=[
                PlaybookStep(
                    id="step-14",
                    order=1,
                    title="Get Memory Metrics",
                    description="Check current memory usage patterns",
                    commands=["kubectl top pods -n production -l app=<service-name>"],
                    links=["https://grafana.company.com/d/memory-usage"],
                    is_automated=True
                ),
                PlaybookStep(
                    id="step-15",
                    order=2,
                    title="Capture Heap Dump",
                    description="Generate heap dump for analysis",
                    commands=[
                        "kubectl exec -it <pod-name> -- jmap -dump:live,format=b,file=/tmp/heapdump.hprof 1",
                        "kubectl cp <pod-name>:/tmp/heapdump.hprof ./heapdump.hprof"
                    ],
                    links=[],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-16",
                    order=3,
                    title="Analyze with Profiler",
                    description="Use memory profiler to identify leak source",
                    commands=[],
                    links=["https://eclipse.org/mat/", "https://visualvm.github.io/"],
                    is_automated=False
                ),
                PlaybookStep(
                    id="step-17",
                    order=4,
                    title="Implement Fix",
                    description="Common fixes include: bounded caches, proper resource cleanup, fixing circular references",
                    commands=[],
                    links=["https://wiki.company.com/memory-leak-patterns"],
                    is_automated=False
                )
            ]
        )
    ]


def get_deployments() -> list[Deployment]:
    """Get sample deployments"""
    return [
        Deployment(
            id="dep-001",
            service="Payment Service",
            version="2.3.4",
            environment=Environment.PRODUCTION,
            status=DeploymentStatus.SUCCESS,
            deployed_at=hours_ago(2),
            deployed_by="charlie@company.com",
            commit_sha="a1b2c3d4e5f6",
            commit_message="feat: Add retry logic for Stripe API calls",
            changed_files=["src/stripe/client.py", "src/stripe/webhook.py", "src/config/retry.py"],
            rollback_available=True
        ),
        Deployment(
            id="dep-002",
            service="User Service",
            version="1.8.2",
            environment=Environment.PRODUCTION,
            status=DeploymentStatus.SUCCESS,
            deployed_at=hours_ago(12),
            deployed_by="eve@company.com",
            commit_sha="f6e5d4c3b2a1",
            commit_message="fix: Implement LRU cache for session validation",
            changed_files=["src/middleware/session.py", "src/cache/lru.py"],
            rollback_available=True
        ),
        Deployment(
            id="dep-003",
            service="API Gateway",
            version="3.1.0",
            environment=Environment.PRODUCTION,
            status=DeploymentStatus.SUCCESS,
            deployed_at=days_ago(1),
            deployed_by="alice@company.com",
            commit_sha="123abc456def",
            commit_message="feat: Add new rate limiting tiers for enterprise customers",
            changed_files=["src/ratelimit/tiers.py", "src/config/enterprise.py", "terraform/ratelimit.tf"],
            rollback_available=True
        ),
        Deployment(
            id="dep-004",
            service="Search Service",
            version="2.0.1",
            environment=Environment.PRODUCTION,
            status=DeploymentStatus.SUCCESS,
            deployed_at=days_ago(2),
            deployed_by="ivan@company.com",
            commit_sha="def456abc123",
            commit_message="chore: Upgrade Elasticsearch client to v8",
            changed_files=["src/elasticsearch/client.py", "requirements.txt", "src/search/queries.py"],
            rollback_available=True
        ),
        Deployment(
            id="dep-005",
            service="Database Cluster",
            version="14.2",
            environment=Environment.PRODUCTION,
            status=DeploymentStatus.SUCCESS,
            deployed_at=days_ago(7),
            deployed_by="george@company.com",
            commit_sha="789xyz012abc",
            commit_message="upgrade: PostgreSQL 14.1 to 14.2 with security patches",
            changed_files=["terraform/database.tf", "ansible/postgres.yml"],
            rollback_available=False
        )
    ]


def get_alerts() -> list[Alert]:
    """Get sample alerts"""
    return [
        Alert(
            id="alert-001",
            title="Payment Error Rate Critical",
            description="Payment error rate exceeded 10% threshold",
            severity=Severity.CRITICAL,
            source="Datadog",
            service="Payment Service",
            status=AlertStatus.FIRING,
            fired_at=minutes_ago(45),
            related_incident_id="inc-001"
        ),
        Alert(
            id="alert-002",
            title="Database Connection Pool Warning",
            description="PostgreSQL connection pool at 85% capacity",
            severity=Severity.HIGH,
            source="Prometheus",
            service="Database Cluster",
            status=AlertStatus.ACKNOWLEDGED,
            fired_at=hours_ago(2) + timedelta(minutes=30),
            acknowledged_at=hours_ago(2),
            acknowledged_by="george@company.com",
            related_incident_id="inc-002"
        ),
        Alert(
            id="alert-003",
            title="Search Latency P99 High",
            description="Search service P99 latency above 1000ms",
            severity=Severity.MEDIUM,
            source="Datadog",
            service="Search Service",
            status=AlertStatus.ACKNOWLEDGED,
            fired_at=hours_ago(4),
            acknowledged_at=hours_ago(3) + timedelta(minutes=30),
            acknowledged_by="ivan@company.com",
            related_incident_id="inc-003"
        ),
        Alert(
            id="alert-004",
            title="API Gateway 5xx Spike",
            description="5xx error rate increased by 50% in last 5 minutes",
            severity=Severity.HIGH,
            source="CloudWatch",
            service="API Gateway",
            status=AlertStatus.RESOLVED,
            fired_at=hours_ago(6),
            resolved_at=hours_ago(5)
        ),
        Alert(
            id="alert-005",
            title="User Service Memory Warning",
            description="Memory usage above 80% threshold",
            severity=Severity.MEDIUM,
            source="Kubernetes",
            service="User Service",
            status=AlertStatus.RESOLVED,
            fired_at=days_ago(3),
            resolved_at=days_ago(2),
            related_incident_id="inc-005"
        )
    ]


# Export all data
INCIDENTS = get_incidents()
PLAYBOOKS = get_playbooks()
DEPLOYMENTS = get_deployments()
ALERTS = get_alerts()
