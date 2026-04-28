# Example: Issue Breakdown - CSV Export

## Independent Testable Stories

### Story 1: Backend Export API
**As** a developer  
**I want** an API endpoint to retrieve user data  
**So that** frontend can trigger exports  

**Acceptance Criteria:**
- GET /api/users/export returns CSV data
- Supports column selection via query params
- Limited to 10,000 rows
- Requires admin authentication

**Linked to:** REQ-1, REQ-2, REQ-3, BS-1, BS-2, BS-3, TS-1

### Story 2: Frontend Export Button
**As** an admin  
**I want** an export button on user list  
**So that** I can download user data  

**Acceptance Criteria:**
- Button visible only to admins
- Triggers download on click
- Shows loading state
- Handles errors gracefully

**Linked to:** REQ-1, BS-1, BS-4, TS-2

### Story 3: Rate Limiting
**As** a system  
**I want** to limit export frequency  
**So that** abuse is prevented  

**Acceptance Criteria:**
- Max 5 exports per hour per user
- Returns 429 when exceeded
- Rate limit resets hourly

**Linked to:** BR-4, BS-5, TS-4

### Story 4: Column Selection UI
**As** an admin  
**I want** to choose export columns  
**So that** I get only needed data  

**Acceptance Criteria:**
- Checkbox interface for column selection
- Defaults to all visible columns
- Persists selection (optional)

**Linked to:** REQ-2, BS-2, TS-5

**Note:** Each story is independent, testable, and links back to requirements/behaviors/tests.