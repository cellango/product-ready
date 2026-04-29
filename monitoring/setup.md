# Monitoring & Observability Setup

## Overview

This guide covers comprehensive monitoring, logging, and observability setup for Product Ready in production environments. It includes metrics collection, logging aggregation, tracing, and alerting configurations.

## Monitoring Architecture

### Three Pillars of Observability

```
1. Metrics
   - Performance indicators (latency, throughput)
   - Resource utilization (CPU, memory)
   - Business metrics (workflows processed)

2. Logging
   - Application logs (debug, info, warnings)
   - Audit logs (compliance, security)
   - Access logs (API usage)

3. Tracing
   - Distributed tracing (request flows)
   - Performance analysis (bottlenecks)
   - Error tracking (exceptions)
```

## Metrics Collection

### Prometheus Setup

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'product-ready'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 5s
    
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Key Metrics

**Workflow Metrics**
```python
from prometheus_client import Counter, Histogram, Gauge

# Counter: Total workflows
workflows_total = Counter(
    'product_ready_workflows_total',
    'Total workflows processed',
    ['mode', 'status', 'provider']
)

# Histogram: Workflow duration
workflow_duration = Histogram(
    'product_ready_workflow_duration_seconds',
    'Workflow execution time',
    ['mode', 'provider'],
    buckets=(1, 5, 10, 25, 50, 100, 250)
)

# Gauge: Active workflows
workflows_active = Gauge(
    'product_ready_workflows_active',
    'Number of active workflows'
)

# Counter: Generated requirements
requirements_generated = Counter(
    'product_ready_requirements_generated_total',
    'Total requirements generated',
    ['requirement_type']
)
```

**System Metrics**
```python
# CPU and Memory
process_cpu_seconds = Counter(
    'process_cpu_seconds_total',
    'Total CPU time'
)

process_memory_bytes = Gauge(
    'process_memory_bytes',
    'Process memory usage'
)

# API Provider Metrics
api_requests = Counter(
    'product_ready_api_requests_total',
    'Total API requests to AI providers',
    ['provider', 'endpoint', 'status']
)

api_latency = Histogram(
    'product_ready_api_latency_seconds',
    'API request latency',
    ['provider'],
    buckets=(0.1, 0.5, 1, 5, 10, 30)
)

# Queue Metrics
queue_depth = Gauge(
    'product_ready_queue_depth',
    'Current workflow queue depth'
)

queue_wait_time = Histogram(
    'product_ready_queue_wait_seconds',
    'Time workflows spend in queue',
    buckets=(1, 5, 10, 30, 60)
)
```

## Logging System

### Structured Logging

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_event(self, level: str, event: str, **context):
        """Log structured event with context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "level": level,
            "service": "product-ready",
            **context
        }
        
        if level == "error":
            self.logger.error(json.dumps(log_entry))
        elif level == "warning":
            self.logger.warning(json.dumps(log_entry))
        elif level == "info":
            self.logger.info(json.dumps(log_entry))
        else:
            self.logger.debug(json.dumps(log_entry))
    
    def log_workflow_start(self, workflow_id: str, mode: str):
        self.log_event(
            "info",
            "workflow_started",
            workflow_id=workflow_id,
            mode=mode
        )
    
    def log_workflow_complete(self, workflow_id: str, duration_ms: int):
        self.log_event(
            "info",
            "workflow_completed",
            workflow_id=workflow_id,
            duration_ms=duration_ms
        )
    
    def log_workflow_error(self, workflow_id: str, error: str):
        self.log_event(
            "error",
            "workflow_failed",
            workflow_id=workflow_id,
            error=error
        )
```

### Logging Configuration

```yaml
# logging.yaml
version: 1
disable_existing_loggers: false

formatters:
  json:
    class: pythonjsonlogger.jsonlogger.JsonFormatter
    format: "%(timestamp)s %(level)s %(name)s %(message)s"
  
  standard:
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: json
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: json
    filename: logs/product-ready.log
    maxBytes: 10485760  # 10MB
    backupCount: 10
  
  audit:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: json
    filename: logs/audit.log
    maxBytes: 10485760
    backupCount: 30

root:
  level: INFO
  handlers: [console, file]

loggers:
  product_ready.audit:
    level: INFO
    handlers: [audit]
    propagate: false
```

### Audit Logging

```python
class AuditLogger:
    """Log security and compliance events"""
    
    def __init__(self):
        self.logger = logging.getLogger('product_ready.audit')
    
    def log_api_key_access(self, user: str, provider: str):
        """Log API key access for compliance"""
        self.logger.info(
            "API key accessed",
            extra={
                "event_type": "api_key_access",
                "user": user,
                "provider": provider,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def log_data_export(self, user: str, data_type: str, record_count: int):
        """Log data exports for GDPR compliance"""
        self.logger.info(
            "Data exported",
            extra={
                "event_type": "data_export",
                "user": user,
                "data_type": data_type,
                "record_count": record_count
            }
        )
    
    def log_compliance_check(self, check_name: str, status: str):
        """Log compliance check results"""
        self.logger.info(
            "Compliance check",
            extra={
                "event_type": "compliance_check",
                "check_name": check_name,
                "status": status
            }
        )
```

## Distributed Tracing

### OpenTelemetry Setup

```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Set trace provider
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Get tracer
tracer = trace.get_tracer(__name__)

# Instrument workflows
def process_workflow_traced(idea: str):
    with tracer.start_as_current_span("process_workflow") as span:
        span.set_attribute("product.idea_length", len(idea))
        
        with tracer.start_as_current_span("generate_requirements") as child_span:
            requirements = generate_requirements(idea)
            child_span.set_attribute("requirement_count", len(requirements))
        
        with tracer.start_as_current_span("generate_spec") as child_span:
            spec = generate_spec(requirements)
            child_span.set_attribute("spec_size", len(spec))
        
        return {"requirements": requirements, "spec": spec}
```

## Alerting Rules

### Alert Definitions

```yaml
# alerts.yml
groups:
  - name: product_ready
    rules:
      # Performance Alerts
      - alert: HighWorkflowLatency
        expr: histogram_quantile(0.95, product_ready_workflow_duration_seconds) > 10
        for: 5m
        annotations:
          summary: "High workflow latency"
          description: "P95 latency is {{ $value }}s"
      
      # Error Rate Alerts
      - alert: HighErrorRate
        expr: |
          rate(product_ready_workflows_total{status="error"}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High workflow error rate"
          description: "Error rate is {{ $value | humanizePercentage }}"
      
      # Resource Alerts
      - alert: HighMemoryUsage
        expr: process_memory_bytes > 1073741824  # 1GB
        for: 5m
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanize }}B"
      
      # API Provider Alerts
      - alert: APIProviderDown
        expr: up{job="anthropic-api"} == 0
        for: 1m
        annotations:
          summary: "API provider unreachable"
          description: "{{ $labels.provider }} is down"
      
      # Queue Alerts
      - alert: LargeQueueDepth
        expr: product_ready_queue_depth > 1000
        for: 5m
        annotations:
          summary: "Large workflow queue"
          description: "Queue depth is {{ $value }} workflows"
```

### Notification Channels

```python
class AlertNotifier:
    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
        self.pagerduty_key = os.getenv("PAGERDUTY_KEY")
    
    def send_slack_alert(self, alert: str, severity: str):
        """Send alert to Slack"""
        color = {
            "critical": "#FF0000",
            "warning": "#FFA500",
            "info": "#00FF00"
        }[severity]
        
        payload = {
            "attachments": [{
                "color": color,
                "title": "Product Ready Alert",
                "text": alert,
                "ts": int(time.time())
            }]
        }
        
        requests.post(self.slack_webhook, json=payload)
    
    def send_pagerduty_alert(self, alert: str, severity: str):
        """Trigger PagerDuty incident"""
        payload = {
            "routing_key": self.pagerduty_key,
            "event_action": "trigger",
            "payload": {
                "summary": alert,
                "severity": severity,
                "source": "product-ready",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            json=payload
        )
```

## Dashboards

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Product Ready - Production Dashboard",
    "panels": [
      {
        "title": "Workflow Throughput",
        "targets": [{
          "expr": "rate(product_ready_workflows_total[5m])"
        }],
        "type": "graph"
      },
      {
        "title": "Latency (P95)",
        "targets": [{
          "expr": "histogram_quantile(0.95, product_ready_workflow_duration_seconds)"
        }],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "rate(product_ready_workflows_total{status=\"error\"}[5m])"
        }],
        "type": "graph"
      },
      {
        "title": "Resource Utilization",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total[5m])",
            "legendFormat": "CPU"
          },
          {
            "expr": "process_memory_bytes / 1024 / 1024",
            "legendFormat": "Memory (MB)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Queue Depth",
        "targets": [{
          "expr": "product_ready_queue_depth"
        }],
        "type": "graph"
      },
      {
        "title": "API Provider Health",
        "targets": [{
          "expr": "up{job=~\"anthropic|openai\"}"
        }],
        "type": "table"
      }
    ]
  }
}
```

## Health Checks

### Liveness and Readiness Probes

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health/live', methods=['GET'])
def liveness_probe():
    """Kubernetes liveness probe - process still running?"""
    return jsonify({"status": "alive"}), 200

@app.route('/health/ready', methods=['GET'])
def readiness_probe():
    """Kubernetes readiness probe - ready for traffic?"""
    checks = {
        "database": check_database_connection(),
        "api_provider": check_api_provider_connection(),
        "queue": check_queue_health(),
        "disk": check_disk_space()
    }
    
    if all(checks.values()):
        return jsonify({"status": "ready", "checks": checks}), 200
    else:
        return jsonify({"status": "not_ready", "checks": checks}), 503

def check_api_provider_connection():
    try:
        response = requests.get(
            "https://api.anthropic.com/health",
            timeout=5
        )
        return response.status_code == 200
    except:
        return False
```

## Deployment Configuration

### Docker Compose with Monitoring

```yaml
version: '3.8'

services:
  product-ready:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PROMETHEUS_PORT=8001
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
  
  jaeger:
    image: jaegertracing/all-in-one
    ports:
      - "6831:6831/udp"
      - "16686:16686"

volumes:
  prometheus-data:
  grafana-data:
```

## Monitoring Checklist

- [ ] Prometheus configured and scraping metrics
- [ ] Grafana dashboards created and deployed
- [ ] Alerting rules configured
- [ ] Notification channels (Slack, PagerDuty) integrated
- [ ] Structured logging implemented
- [ ] Audit logging enabled
- [ ] Distributed tracing (Jaeger) set up
- [ ] Health checks implemented
- [ ] SLA monitoring configured
- [ ] Runbooks created for common alerts

## SLA & Service Metrics

```
Service Level Objectives:
- Availability: 99.9% (target 99.95%)
- Latency (p95): < 25 seconds for Standard mode
- Error Rate: < 0.5%
- Queue Wait: < 5 seconds average

Incident Response:
- Critical: Page on-call within 5 minutes
- High: Notify team within 30 minutes
- Medium: Address within 2 hours
- Low: Track for next sprint
```

---

*Monitoring guide last updated: April 28, 2026*