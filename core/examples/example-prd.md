# Example: PRD - CSV Export Feature

## Product Requirements Document

### Business Objective
Enable admins to export user data for reporting and compliance purposes.

### Customer Problem
Admins need to analyze user data outside the system, but currently must manually copy-paste or use workarounds.

### Success Metric (SMART)
- **Specific:** 80% of admins use export feature weekly
- **Measurable:** Track downloads via analytics
- **Achievable:** Based on user feedback
- **Relevant:** Improves admin efficiency
- **Time-bound:** Achieve within 3 months post-launch
- **Integrity:** Baseline: 0%, Target: 80%, Timeframe: 3 months, Decision rule: If <60% after 1 month, investigate barriers

### Requirements
- **REQ-1:** Export button on user list page
- **REQ-2:** CSV format with configurable columns
- **REQ-3:** Secure access (admin role required)
- **REQ-4:** Asynchronous download for large datasets

### Business Rules
- **BR-1:** Only active users included by default
- **BR-2:** Sensitive fields (passwords) never exported
- **BR-3:** Max 10,000 rows per export
- **BR-4:** Rate limit: 5 exports per hour per user

### Goals and Non-Goals
- **Goal:** Simple, reliable export
- **Non-Goal:** Advanced filtering (use existing table filters)
- **Non-Goal:** Multiple formats (start with CSV)

### Dependencies
- Backend: API endpoint for data retrieval
- Frontend: Download handling
- Security: Role-based access control