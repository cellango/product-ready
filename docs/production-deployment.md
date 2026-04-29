# Production Deployment Guide

## Overview

This guide covers deploying Product Ready to production environments, including infrastructure setup, configuration management, deployment strategies, and operational procedures.

## Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Load balancer configured (AWS ALB, GCP LB, etc.)
- [ ] Database or persistent storage ready
- [ ] API credentials (Anthropic, OpenAI) provisioned
- [ ] SSL/TLS certificates installed
- [ ] DNS configured
- [ ] Backup and recovery systems in place
- [ ] Monitoring infrastructure deployed
- [ ] Log aggregation system ready

### Compliance & Security
- [ ] Security audit completed
- [ ] Penetration testing finished
- [ ] GDPR/HIPAA/SOC2 assessments done
- [ ] Access control and RBAC configured
- [ ] Secrets management system deployed
- [ ] Security scanning enabled in CI/CD
- [ ] Incident response plan documented
- [ ] Data retention policies configured

### Testing & Validation
- [ ] Load testing completed (see Performance Guide)
- [ ] Canary deployment tested
- [ ] Rollback procedure tested
- [ ] Disaster recovery tested
- [ ] Health checks validated
- [ ] Monitoring alerts tested
- [ ] Documentation complete and current
- [ ] Team training completed

## Deployment Architectures

### Single-Region Deployment (Small/Medium)

```
┌─────────────────────────────────────┐
│          Users / API Clients         │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      │   ALB/LB    │ (SSL/TLS)
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │  Auto-Scale │
      │   Group     │
      └──────┬──────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──┐  ┌───┬──┐  ┌─▼───┐
│Pod 1 │  │Pod│..│  │Pod N│
└───┬──┘  └───┴──┘  └─┬───┘
    │        │        │
    └────────┬────────┘
             │
      ┌──────▼───────┐
      │ RDS Database │
      └──────────────┘
      
      ┌────────────────┐
      │Monitoring Stack│
      │- Prometheus   │
      │- Grafana      │
      │- Alerting     │
      └────────────────┘
```

### Multi-Region Deployment (Enterprise)

```
Region 1 (Primary)          Region 2 (Backup)
┌─────────────────┐         ┌─────────────────┐
│   ALB (US-E)    │         │   ALB (EU-W)    │
└────────┬────────┘         └────────┬────────┘
         │                           │
    ┌────▼────┐               ┌────▼────┐
    │Pod Pool │               │Pod Pool │
    │   x3    │               │   x3    │
    └────┬────┘               └────┬────┘
         │                         │
    ┌────▼────┐               ┌────▼────┐
    │RDS - US │───Replication│RDS - EU │
    └─────────┘               └─────────┘
    
    Global Load Balancer
    (Route53, Cloud Armor)
    
    Shared: Monitoring, Logging, Secrets Manager
```

## Kubernetes Deployment

### Namespace Setup

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: product-ready
  labels:
    environment: production
    monitoring: enabled
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: product-ready-quota
  namespace: product-ready
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "100"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: product-ready-limits
  namespace: product-ready
spec:
  limits:
  - max:
      cpu: "2"
      memory: "4Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
    type: Container
```

### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-ready
  namespace: product-ready
  labels:
    app: product-ready
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  
  selector:
    matchLabels:
      app: product-ready
  
  template:
    metadata:
      labels:
        app: product-ready
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8001"
        prometheus.io/path: "/metrics"
    
    spec:
      # Security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      
      # Service account
      serviceAccountName: product-ready
      
      # Containers
      containers:
      - name: product-ready
        image: product-ready:1.0.0
        imagePullPolicy: IfNotPresent
        
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        - name: metrics
          containerPort: 8001
          protocol: TCP
        
        # Environment variables
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: product-ready-secrets
              key: anthropic-api-key
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: product-ready-secrets
              key: openai-api-key
        
        # Resource limits
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1024Mi"
        
        # Health checks
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        
        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        
        # Volume mounts
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: logs
          mountPath: /var/log/product-ready
      
      # Volumes
      volumes:
      - name: tmp
        emptyDir: {}
      - name: logs
        emptyDir: {}
      
      # Pod disruption budget
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - product-ready
              topologyKey: kubernetes.io/hostname

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: product-ready-pdb
  namespace: product-ready
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: product-ready
```

### Service & Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: product-ready
  namespace: product-ready
spec:
  type: ClusterIP
  selector:
    app: product-ready
  ports:
  - name: http
    port: 80
    targetPort: http
  - name: metrics
    port: 8001
    targetPort: metrics

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: product-ready
  namespace: product-ready
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.product-ready.dev
    secretName: product-ready-tls
  rules:
  - host: api.product-ready.dev
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: product-ready
            port:
              number: 80
```

### Secrets Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: product-ready-secrets
  namespace: product-ready
type: Opaque
stringData:
  anthropic-api-key: ${ANTHROPIC_API_KEY}
  openai-api-key: ${OPENAI_API_KEY}
  database-url: ${DATABASE_URL}
```

## Cloud-Specific Deployment

### AWS ECS Deployment

```json
{
  "family": "product-ready",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "product-ready",
      "image": "product-ready:1.0.0",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        },
        {
          "containerPort": 8001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:anthropic-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/product-ready",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health/live || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 30
      }
    }
  ]
}
```

### Google Cloud Run Deployment

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: product-ready
  namespace: default
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "3"
        autoscaling.knative.dev/maxScale: "100"
    spec:
      containers:
      - image: gcr.io/project-id/product-ready:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: production
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: product-ready-secrets
              key: anthropic-api-key
        resources:
          limits:
            cpu: "1000m"
            memory: "512Mi"
```

## Deployment Strategies

### Blue-Green Deployment

```bash
#!/bin/bash

# 1. Deploy new version to green environment
kubectl set image deployment/product-ready-green \
  product-ready=product-ready:v2.0.0 \
  -n product-ready

# 2. Wait for green to be ready
kubectl wait --for=condition=available \
  --timeout=300s \
  deployment/product-ready-green \
  -n product-ready

# 3. Run smoke tests against green
./smoke-tests.sh green

# 4. If successful, switch traffic to green
kubectl patch service product-ready \
  -p '{"spec":{"selector":{"version":"v2.0.0"}}}' \
  -n product-ready

# 5. Monitor for issues
sleep 300 && ./monitor.sh

# 6. If issues, rollback to blue
kubectl patch service product-ready \
  -p '{"spec":{"selector":{"version":"v1.0.0"}}}' \
  -n product-ready
```

### Canary Deployment

```bash
#!/bin/bash

# 1. Deploy canary with 10% traffic
kubectl apply -f canary-deployment.yaml

# 2. Monitor metrics (5 minutes)
# - Error rate
# - Latency
# - Custom metrics
sleep 300

# 3. Gradually increase traffic
for percentage in 25 50 75 100; do
  kubectl patch virtualservice product-ready \
    --type merge \
    -p "{\"spec\":{\"hosts\":[{\"name\":\"product-ready\",\"http\":[{\"match\":[{\"uri\":{\"prefix\":\"/\"}}],\"route\":[{\"destination\":{\"host\":\"product-ready-v1\"},\"weight\":$((100-percentage))},{\"destination\":{\"host\":\"product-ready-v2\"},\"weight\":$percentage}]}]}]}}"
  
  sleep 300
  if ! ./health-check.sh; then
    echo "Canary failed, rolling back..."
    exit 1
  fi
done
```

## Post-Deployment Procedures

### Smoke Tests

```bash
#!/bin/bash

# Health checks
curl -f http://localhost/health/live
curl -f http://localhost/health/ready

# API endpoint tests
curl -X POST http://localhost/api/workflow \
  -H "Content-Type: application/json" \
  -d '{"idea": "Simple feature request"}'

# Performance baseline
ab -n 100 -c 10 http://localhost/

# Log verification
grep ERROR /var/log/product-ready/application.log && exit 1
echo "✓ Smoke tests passed"
```

### Production Monitoring

```bash
# Check deployment status
kubectl get deployment product-ready -n product-ready
kubectl get pods -n product-ready

# Check metrics
curl http://prometheus:9090/api/v1/query?query=up{job=\"product-ready\"}

# View logs
kubectl logs -f deployment/product-ready -n product-ready

# Describe service
kubectl describe service product-ready -n product-ready
```

## Rollback Procedures

### Kubernetes Rollback

```bash
# View deployment history
kubectl rollout history deployment/product-ready -n product-ready

# Rollback to previous version
kubectl rollout undo deployment/product-ready -n product-ready

# Rollback to specific revision
kubectl rollout undo deployment/product-ready \
  --to-revision=2 \
  -n product-ready

# Monitor rollback progress
kubectl rollout status deployment/product-ready -n product-ready
```

### Database Rollback

```bash
# If migrations failed, restore from backup
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier product-ready-prod \
  --db-snapshot-identifier product-ready-snapshot-2026-04-28

# Update DNS to point to restored instance
# Run smoke tests to verify
```

## Disaster Recovery

### Backup Strategy

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: product-ready-daily
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  template:
    includedNamespaces:
    - product-ready
    storageLocation: aws-s3
    volumeSnapshotLocation: aws-ebs
    ttl: 720h  # 30 days
```

### Recovery Plan

```
Recovery Time Objective (RTO): 4 hours
Recovery Point Objective (RPO): 1 hour

1. Infrastructure Recovery (30 min)
   - Restore network configuration
   - Recreate Kubernetes cluster
   - Restore persistent volumes

2. Application Recovery (1 hour)
   - Restore from Velero backup
   - Verify health checks
   - Run smoke tests

3. Data Recovery (30 min)
   - Restore database from snapshot
   - Run integrity checks

4. Validation (30 min)
   - Full test suite
   - User acceptance testing
```

## Scaling Configuration

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: product-ready-hpa
  namespace: product-ready
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-ready
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

## Documentation & Runbooks

### Production Runbooks
- [ ] Deployment runbook
- [ ] Rollback runbook
- [ ] Incident response runbook
- [ ] Database recovery runbook
- [ ] High load procedures
- [ ] Security incident procedures

---

*Production deployment guide last updated: April 28, 2026*