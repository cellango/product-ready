# Example: Behavior Spec (BDD) - CSV Export

## Behavior Scenarios

### BS-1: Successful Export (Must)
**Given** admin is logged in and viewing user list  
**When** clicks "Export CSV" button  
**Then** CSV file downloads with user data  
**And** file includes columns: Name, Email, Registration Date, Status  
**And** only active users are included  

### BS-2: Column Selection (Should)
**Given** admin selects custom columns  
**When** clicks "Export CSV"  
**Then** CSV includes only selected columns  

### BS-3: Large Dataset (Must)
**Given** user list has 10,001 users  
**When** clicks "Export CSV"  
**Then** export is limited to 10,000 rows  
**And** user sees warning message  

### BS-4: Access Denied (Must)
**Given** non-admin user views user list  
**When** looks for export button  
**Then** export button is not visible  

### BS-5: Rate Limit Exceeded (Should)
**Given** admin has exported 5 times in last hour  
**When** clicks "Export CSV"  
**Then** sees error: "Export limit reached, try again later"  

### Edge Cases
- Empty user list: Download empty CSV with headers
- Special characters in names: Properly encoded in CSV
- Network failure: Retry mechanism or clear error

### Failure Cases
- File download fails: Show error message
- Data corruption: Validate CSV integrity

### UI States
- Loading: Spinner during export preparation
- Success: Download notification
- Error: Inline error message

### Observable Outputs
- CSV file content matches database
- Audit log entry for each export