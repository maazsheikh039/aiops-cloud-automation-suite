#!/usr/bin/env python3
import yaml
import json
import os
from pathlib import Path
from datetime import datetime
from audit_logger import AuditLogger

class ApprovalEngine:
    def __init__(self, config_path="config/approval_rules.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.state_file = "approval_state.json"
        self.audit_logger = AuditLogger(self.config.get("audit_settings", {}).get("log_directory", "logs"))
        self.state = self._load_state()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return {"approval_gates": []}
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def _get_applicable_gate(self, amount):
        gates = sorted(self.config.get("approval_gates", []), key=lambda x: x.get("threshold", 0))
        selected_gate = None
        for gate in gates:
            if amount >= gate.get("threshold", 0):
                selected_gate = gate
        return selected_gate

    def request_approval(self, request_data):
        req_id = request_data.get("request_id") or f"REQ-{int(datetime.now().timestamp())}"
        amount = float(request_data.get("amount", 0))
        requester = request_data.get("requester", "unknown")
        description = request_data.get("description", "")

        gate = self._get_applicable_gate(amount)
        gate_name = gate.get("name") if gate else "auto_approved"
        required_approvals = gate.get("required_approvals", 0) if gate else 0
        approvers_list = gate.get("approvers", []) if gate else []

        record = {
            "request_id": req_id,
            "amount": amount,
            "requester": requester,
            "description": description,
            "gate": gate_name,
            "required_approvals": required_approvals,
            "authorized_approvers": approvers_list,
            "approvals": [],
            "status": "APPROVED" if required_approvals == 0 else "PENDING",
            "created_at": datetime.now().isoformat()
        }

        self.state[req_id] = record
        self._save_state()

        self.audit_logger.log_event("request_created", record)
        return record

    def approve_request(self, request_id, approver):
        if request_id not in self.state:
            return {"error": "Request ID not found"}

        req = self.state[request_id]
        if req["status"] == "APPROVED":
            return {"message": "Request already fully approved.", "status": "APPROVED"}

        if approver not in req["authorized_approvers"]:
            return {"error": f"User '{approver}' is not authorized to approve this gate."}

        if approver in req["approvals"]:
            return {"message": f"User '{approver}' has already approved this request."}

        req["approvals"].append(approver)
        
        event_data = {"request_id": request_id, "approver": approver}
        self.audit_logger.log_event("approval_recorded", event_data)

        if len(req["approvals"]) >= req["required_approvals"]:
            req["status"] = "APPROVED"
            self.audit_logger.log_event("request_fully_approved", {"request_id": request_id})

        self._save_state()
        return req

    def get_request_status(self, request_id):
        if request_id not in self.state:
            return {"error": "Request ID not found"}
        return self.state[request_id]
