#!/bin/bash
echo "=== Testing Finance Approval System ==="

# 1. Create a high-value request ($2000 triggers budget_review gate requiring 2 approvals)
REQ_JSON=$(python3 workflows/approval_cli.py request --amount 2000 --requester dev_user --description "Production AWS Cluster Upgrade")
echo "$REQ_JSON"

# Extract Request ID using python
REQ_ID=$(python3 -c "import json; data = json.load(open('approval_state.json')); print(list(data.keys())[-1])")
echo "Extracted Request ID: $REQ_ID"

# 2. First Approval by finance_manager
python3 workflows/approval_cli.py approve --request-id "$REQ_ID" --approver finance_manager

# 3. Check Status (should still be PENDING since required_approvals = 2)
python3 workflows/approval_cli.py status --request-id "$REQ_ID"

# 4. Second Approval by team_lead
python3 workflows/approval_cli.py approve --request-id "$REQ_ID" --approver team_lead

# 5. Check Final Status (should now be APPROVED)
python3 workflows/approval_cli.py status --request-id "$REQ_ID"

# 6. Query Audit Logs
python3 workflows/audit_query.py --days 1
python3 workflows/audit_query.py --report --days 1
