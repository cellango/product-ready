# Service Level Agreement (SLA) & Support

## SLA Overview

Product Ready provides tiered service level agreements based on deployment and support tiers. This document outlines commitments, definitions, and support procedures.

## Tier Definitions

### Community Tier (Free)
- **Best For**: Individual developers, small teams, learning
- **Support**: Community-driven (GitHub discussions)
- **SLA**: Best-effort, no formal commitments
- **Cost**: Free

### Professional Tier (Paid)
- **Best For**: Product teams, startups, small enterprises
- **Support**: Email-based support, 48-hour response time
- **SLA**: 99.5% availability (3.6 hours downtime/month)
- **Cost**: $99/month

### Enterprise Tier (Paid)
- **Best For**: Large organizations, regulated industries
- **Support**: 24/7 phone/email, dedicated support engineer
- **SLA**: 99.99% availability (5 minutes downtime/month)
- **Cost**: Custom pricing

### Enterprise Plus Tier (Premium)
- **Best For**: Mission-critical deployments
- **Support**: 24/7 phone/email, dedicated team, architect support
- **SLA**: 99.999% availability (26 seconds downtime/month)
- **Cost**: Custom pricing + minimum $50K/year

## Availability SLAs

### Availability Definition
Service is considered "available" when:
- API responds to requests within defined latency
- Workflow execution succeeds or fails gracefully
- Monitoring and alerting systems functional
- No data loss or corruption

### Planned Maintenance Exclusions
- Scheduled maintenance windows (24-hour notice)
- Emergency security patches (best-effort notice)
- Force majeure events (natural disasters, etc.)

### SLA Calculation

```
Uptime % = (Total Time - Downtime) / Total Time × 100

Example:
Month = 30 days = 43,200 minutes
Downtime = 21.6 minutes (99.95% SLA)
Uptime = 43,200 - 21.6 = 43,178.4 minutes
Uptime % = 43,178.4 / 43,200 = 99.95%
```

### Monthly SLA Targets

| Tier | SLA Target | Allowed Downtime | Credit |
|------|-----------|-----------------|--------|
| Professional | 99.5% | 3.6 hours | 10% |
| Enterprise | 99.99% | 4.3 minutes | 25% |
| Enterprise Plus | 99.999% | 26 seconds | 50% |

## Performance SLAs

### Response Time Targets (p95)

| Mode | Professional | Enterprise | Enterprise Plus |
|------|-------------|-----------|-----------------|
| Lightweight | < 8s | < 5s | < 3s |
| Standard | < 20s | < 15s | < 10s |
| Full | < 60s | < 45s | < 30s |

### Throughput Guarantees

| Tier | Workflows/Minute | Concurrent Users | API Requests/Hour |
|------|------------------|------------------|-------------------|
| Professional | 50 | 10 | 500 |
| Enterprise | 500 | 100 | 5,000 |
| Enterprise Plus | 2,000 | 500 | 20,000 |

### Query Performance

- Average response time: As defined above
- P99 response time: 2x average
- Error rate: < 0.1%
- Timeout failures: < 0.05%

## Support SLAs

### Support Channel Availability

| Tier | Email | Chat | Phone | Dedicated |
|------|-------|------|-------|-----------|
| Professional | 24/7 | No | No | No |
| Enterprise | 24/7 | 9-5 | 9-5 | No |
| Enterprise Plus | 24/7 | 24/7 | 24/7 | Yes |

### Response Time Commitments

**Professional Tier**
```
Priority | Response Time | Resolution Time
---------|---------------|----------------
Critical | 24 hours      | 5 business days
High     | 48 hours      | 10 business days
Medium   | 72 hours      | 15 business days
Low      | 1 week        | 30 business days
```

**Enterprise Tier**
```
Priority | Response Time | Resolution Time
---------|---------------|----------------
Critical | 4 hours       | 1 business day
High     | 8 hours       | 2 business days
Medium   | 1 business day| 5 business days
Low      | 2 days        | 10 business days
```

**Enterprise Plus Tier**
```
Priority | Response Time | Resolution Time
---------|---------------|----------------
Critical | 1 hour        | 4 hours
High     | 2 hours       | 1 business day
Medium   | 4 hours       | 3 business days
Low      | 1 business day| 7 business days
```

### Priority Definitions

**Critical**
- Production system down or severely impaired
- Data loss or corruption
- Security vulnerability exploited
- Complete feature unavailability
- Example: "Workflows failing 100%, entire API offline"

**High**
- Major functionality impaired
- Significant performance degradation
- Workaround not available
- Multiple users affected
- Example: "Requirement generation takes 5 minutes instead of 20 seconds"

**Medium**
- Feature partially working or degraded
- Workaround available
- Limited user impact
- Example: "Compliance guardrails not showing in UI but functionality intact"

**Low**
- Minor issue or enhancement
- No impact on functionality
- Documentation clarification
- Example: "Typo in error message"

## Incident Management

### Incident Reporting

**Report an Incident**:
1. Professional: Email support@product-ready.dev
2. Enterprise: Email support@product-ready.dev or call support line
3. Enterprise Plus: Dedicated support engineer contact

**Include**:
- Detailed description of issue
- Steps to reproduce
- Screenshots/logs if applicable
- Affected users/workflows
- Business impact
- System information (version, deployment, OS)

### Incident Response Procedure

```
1. Acknowledgment (within SLA response time)
   - Assign ticket number
   - Assign support engineer
   - Set resolution target

2. Initial Diagnosis (30 minutes)
   - Gather additional information
   - Reproduce issue in lab
   - Assess severity/impact

3. Troubleshooting (ongoing)
   - Execute diagnostic steps
   - Engage engineering if needed
   - Document findings

4. Resolution (within SLA resolution time)
   - Implement fix
   - Test thoroughly
   - Deploy to production
   - Verify with customer

5. Post-Incident (within 2 business days)
   - Send RCA (Root Cause Analysis)
   - Identify preventative measures
   - Schedule follow-up if needed
```

### Escalation Path

**Level 1**: Support Engineer
- Handles routine issues
- Follows troubleshooting procedures
- Can authorize 5% workarounds

**Level 2**: Senior Support Engineer
- Handles complex technical issues
- Can authorize configuration changes
- Can override standard procedures

**Level 3**: Engineering Manager
- Critical issues requiring code changes
- Novel problems requiring development
- Can authorize emergency patches

**Level 4**: VP Engineering
- Mission-critical incidents
- Possible system architecture changes
- Executive communication

## Maintenance Windows

### Scheduled Maintenance

**Standard Window**: Sunday 2:00-6:00 AM UTC
- 24-hour notice provided
- Up to 4 hours downtime allowed
- SLA not charged during window

**Emergency Maintenance**: As needed
- Security patches: 1-hour notice
- Critical fixes: Best-effort notice
- SLA might apply (assessed individually)

### Maintenance Communication

- **Announcement**: Posted 24 hours before (standard) or immediately (emergency)
- **Channel**: Status page, email, Slack integration
- **Details**: Expected duration, affected services, impact
- **Updates**: Provided every 30 minutes during maintenance
- **Completion**: Notification with confirmation of completion

## Credits & Refunds

### Credit Calculation

For Professional/Enterprise tiers, monthly credits applied when uptime falls below target:

```
Uptime Shortfall × 1% of Monthly Fee

Examples:
99.9% actual vs 99.95% target = 0.05% shortfall
Credit = 0.05% × $99 = $0.05

99.9% actual vs 99.99% target = 0.09% shortfall
Credit = 0.09% × $5,000 = $4.50
```

### Credit Limits

- Maximum credit per month: 30% of monthly fee
- Maximum total credits per year: 100% of annual fee
- Credits expire after 12 months
- Non-transferable
- No cash refund (unless otherwise agreed)

### Credit Request Process

1. Customer submits request within 30 days of issue
2. Support verifies downtime via metrics
3. Credit calculated and applied to next invoice
4. Customer notified of credit amount

## SLA Exclusions

Product Ready is not liable under SLAs for:

- Customer application errors or misconfiguration
- Third-party service failures (Anthropic API, OpenAI API, etc.)
- Network connectivity issues
- Customer-provided data quality issues
- Force majeure events (earthquakes, wars, etc.)
- Scheduled maintenance windows
- Beta or preview features
- Community Tier usage

## Enterprise Support Services

### Included Services

**Professional Tier**
- Email support (48-hour response)
- Access to knowledge base
- Community forum
- Monthly technical briefing

**Enterprise Tier**
- Email & chat support (4-hour response for critical)
- Dedicated support engineer (9-5)
- Quarterly business reviews
- Custom training sessions
- Feature prioritization input
- Direct engineer access for technical issues

**Enterprise Plus Tier**
- 24/7 phone & email support (1-hour response for critical)
- Dedicated support team (2-3 people)
- Bi-weekly business reviews
- Custom training and workshops
- Solution architect access
- Direct engineering team access
- Pre-release feature access
- Roadmap influence

### Optional Services

**Custom Implementation**
- Workflow customization: $200/hour
- Integration development: $300/hour
- Compliance consultation: $400/hour

**Training**
- Team training: $2,000/day
- Certification program: $5,000
- Custom workshop: $3,000/day

**Professional Services**
- Architecture review: $10,000
- Security audit: $15,000
- Performance optimization: $10,000

## Monitoring & Metrics

### Public Status Page

- **URL**: status.product-ready.dev
- **Updates**: Every 30 minutes during incidents
- **History**: 90-day uptime history
- **Components**: Individual service status

### Uptime Verification

- Metrics publicly available at: metrics.product-ready.dev
- Third-party monitoring: StatusPage verification
- Independent monitors: Verify from multiple regions
- Audit rights: Enterprise+ can request raw metrics

## Service Review

### Quarterly Reviews

Enterprise+ customers receive:
- Usage and performance reports
- Optimization recommendations
- Roadmap alignment discussion
- Incident review and prevention

### Annual SLA Review

- SLA targets reviewed annually
- Adjustments based on performance
- New requirements discussion
- Pricing evaluation

## Escalation & Complaints

### Formal Complaint Process

1. **Level 1**: Support engineer (first response)
2. **Level 2**: Support manager (within 24 hours)
3. **Level 3**: Director of Support (within 48 hours)
4. **Level 4**: VP Customer Success (within 5 business days)

### Executive Escalation

For unresolved concerns:
- Email: escalation@product-ready.dev
- Include: Previous ticket number, concern summary
- Executive response: Within 2 business days

## SLA Change Policy

- SLA changes: 30-day notice required
- Downgrades: Allowed any time
- Upgrades: Effective immediately
- No retroactive changes
- Existing credits still honored

---

**Effective Date**: April 28, 2026
**Last Updated**: April 28, 2026
**Next Review**: October 28, 2026

For SLA questions: sla@product-ready.dev