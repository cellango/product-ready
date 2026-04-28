# Example: Test Spec - CSV Export

## Test Cases

### TS-1: Basic Export (Automated - Unit)
**Steps:**
1. Mock user data with 3 users
2. Call export API
3. Verify CSV content matches expected format

**Assertions:**
- CSV has correct headers
- All user data present
- No sensitive fields included

**Automation Level:** High (API test)

### TS-2: UI Export Button (Automated - E2E)
**Steps:**
1. Login as admin
2. Navigate to user list
3. Click "Export CSV"
4. Verify file downloads

**Assertions:**
- Button visible only to admins
- Download starts immediately
- File name format: users_export_YYYYMMDD.csv

**Automation Level:** High (Selenium/Playwright)

### TS-3: Large Dataset Handling (Automated - Integration)
**Steps:**
1. Seed database with 15,000 users
2. Trigger export
3. Check response

**Assertions:**
- Only 10,000 rows exported
- Warning message displayed
- No performance degradation >5s

**Automation Level:** Medium (Load test)

### TS-4: Rate Limiting (Automated - API)
**Steps:**
1. Make 6 export requests in <1 hour
2. Verify 6th request fails

**Assertions:**
- HTTP 429 status
- Appropriate error message
- Rate limit resets after 1 hour

**Automation Level:** High (API test)

### TS-5: Column Selection (Manual - Exploratory)
**Steps:**
1. Select subset of columns
2. Export CSV
3. Open in Excel

**Assertions:**
- Only selected columns present
- Data integrity maintained

**Automation Level:** Low (Manual verification)

**Note:** Do not invent rules - all tests derived from BS-* scenarios.