#!/usr/bin/env python3
import yaml
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class PolicyRule:
    id: str
    enabled: bool
    severity: str
    requirement: str
    metadata: Dict = None

class PolicyProfile:
    def __init__(self, profile_data: Dict):
        prof = profile_data.get('profile', {})
        self.name = prof.get('name', 'unknown')
        self.industry = prof.get('industry', 'unknown')
        self.rules: Dict[str, PolicyRule] = {}
        
        for r in prof.get('rules', []):
            rule_id = r.get('id')
            if rule_id:
                self.rules[rule_id] = PolicyRule(
                    id=rule_id,
                    enabled=r.get('enabled', True),
                    severity=r.get('severity', 'medium'),
                    requirement=r.get('requirement', ''),
                    metadata=r
                )
    
    def get_rule(self, rule_id: str) -> Optional[PolicyRule]:
        return self.rules.get(rule_id)
    
    def get_enabled_rules(self) -> List[PolicyRule]:
        return [r for r in self.rules.values() if r.enabled]

class PolicyGate:
    def __init__(self):
        self.profiles: Dict[str, PolicyProfile] = {}
        self.active_profile: Optional[str] = None
    
    def load_profile(self, profile_path: str) -> None:
        with open(profile_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            profile = PolicyProfile(data)
            self.profiles[profile.name] = profile
            if not self.active_profile:
                self.active_profile = profile.name
    
    def switch_profile(self, profile_name: str) -> bool:
        if profile_name in self.profiles:
            self.active_profile = profile_name
            return True
        return False
    
    def enforce_policy(self, request_data: Dict) -> Dict:
        if not self.active_profile or self.active_profile not in self.profiles:
            return {"compliant": False, "error": "No active profile loaded"}
            
        profile = self.profiles[self.active_profile]
        violations = []
        
        for rule in profile.get_enabled_rules():
            if rule.id == "data_encryption":
                if not request_data.get("encrypted", False):
                    violations.append({
                        "rule_id": rule.id,
                        "severity": rule.severity,
                        "requirement": rule.requirement,
                        "message": "Data encryption requirement not met."
                    })
            elif rule.id == "access_logging":
                if not request_data.get("access_logged", False):
                    violations.append({
                        "rule_id": rule.id,
                        "severity": rule.severity,
                        "requirement": rule.requirement,
                        "message": "Access logging not enabled."
                    })
            elif rule.id == "network_segmentation":
                if not request_data.get("network_segmented", False):
                    violations.append({
                        "rule_id": rule.id,
                        "severity": rule.severity,
                        "requirement": rule.requirement,
                        "message": "Network segmentation requirement violated."
                    })
            elif rule.id == "access_control":
                min_len = rule.metadata.get("min_password_length", 8)
                if request_data.get("password_length", 0) < min_len:
                    violations.append({
                        "rule_id": rule.id,
                        "severity": rule.severity,
                        "requirement": rule.requirement,
                        "message": f"Password length must be at least {min_len} characters."
                    })
            elif rule.id == "rate_limiting":
                max_req = rule.metadata.get("max_requests", 1000)
                if request_data.get("request_count", 0) > max_req:
                    violations.append({
                        "rule_id": rule.id,
                        "severity": rule.severity,
                        "requirement": rule.requirement,
                        "message": f"Rate limit exceeded (max {max_req})."
                    })
                    
        return {
            "compliant": len(violations) == 0,
            "active_profile": profile.name,
            "industry": profile.industry,
            "violations": violations
        }
    
    def get_active_profile_info(self) -> Dict:
        if not self.active_profile or self.active_profile not in self.profiles:
            return {"active_profile": None}
        p = self.profiles[self.active_profile]
        return {
            "active_profile": p.name,
            "industry": p.industry,
            "rules_count": len(p.rules),
            "enabled_rules": [r.id for r in p.get_enabled_rules()]
        }
