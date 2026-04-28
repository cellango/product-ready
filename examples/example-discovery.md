# Example: Discovery / Validation

**User Request:** "We want to add export to CSV for our user list."

## Discovery Output

### Problem Clarification
- **What data?** User list data (name, email, registration date, status)
- **Where from?** Admin dashboard user management page
- **Who uses it?** Admins and managers for reporting and compliance
- **Current workflow:** Users view list in table, no export option

### Desired Outcome
- Download CSV file with filtered user data
- Include all visible columns plus optional fields
- Secure: only authorized users can export

### Assumptions Validation
- Assumption: CSV is sufficient (validated: yes, standard format)
- Assumption: No PII concerns (validated: anonymize sensitive data)
- Cheapest test: Prototype with sample data

### Success/Failure Criteria
- Success: CSV downloads correctly with expected data
- Failure: Errors in download, missing data, security breach