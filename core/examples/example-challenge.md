# Example: Challenge (Drill-Me)

**Context:** Following discovery for CSV export feature.

## Challenge Evaluation

### Assumptions Critiqued
- **CSV format assumption:** Is CSV the best? Alternatives: Excel, JSON, PDF. Evidence: Weak - user didn't specify, but CSV is common for data export.
- **Data scope:** Export all users? Risk: Performance for large datasets (10k+ users). Evidence: Medium - need to check current user count.

### Risks Assessment
- **Value:** Low - basic feature, but improves usability
- **Usability:** Medium - need to ensure intuitive placement (e.g., button near table)
- **Feasibility:** High - simple backend addition
- **Viability:** High - no cost impact

### Missing Decisions
- **Missing Product Decision:** What columns to include? Default visible + optional?
- **Missing Product Decision:** File naming convention? "users_export_YYYYMMDD.csv"
- **Missing Product Decision:** Rate limiting? Prevent abuse.

### Simpler Alternatives
- Email report instead of download
- Print-friendly view
- Integration with existing reporting tools

**Recommendation:** Proceed with CSV export, but clarify missing decisions. Escalate to Standard mode due to potential performance risk.