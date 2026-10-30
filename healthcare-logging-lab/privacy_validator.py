import re
import json
import sys

class PrivacyValidator:
    """Validates that logs contain no exposed PII."""
    
    def __init__(self):
        self.violations = []
        self.rules = {
            'ssn_exposed': r'\b\d{3}-\d{2}-\d{4}\b',
            'full_email': r'\b[A-Za-z0-9._%+-]{2,}@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'full_phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        }
    
    def check_record(self, record: dict, line_num: int) -> list:
        violations = []
        record_str = json.dumps(record)
        
        for rule_name, pattern in self.rules.items():
            matches = re.findall(pattern, record_str)
            if matches:
                # Allow masked SSN format (XXX-XX-XXXX)
                if rule_name == 'ssn_exposed' and any('XXX' in m for m in matches):
                    continue
                violations.append({
                    'line': line_num,
                    'rule': rule_name,
                    'matched': matches
                })
                
        if 'ip_address' in record:
            violations.append({
                'line': line_num,
                'rule': 'ip_address_field_present',
                'matched': record['ip_address']
            })
            
        return violations
    
    def validate_file(self, filename: str) -> bool:
        self.violations = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    vols = self.check_record(record, line_num)
                    if vols:
                        self.violations.extend(vols)
                except json.JSONDecodeError:
                    continue
        return len(self.violations) == 0
    
    def generate_report(self):
        print(f"Total violations found: {len(self.violations)}")
        for v in self.violations[:10]:
            print(f"Line {v['line']}: Rule '{v['rule']}' triggered by {v['matched']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 privacy_validator.py <log_file>")
        sys.exit(1)
    
    validator = PrivacyValidator()
    is_compliant = validator.validate_file(sys.argv[1])
    
    if is_compliant:
        print("\n✓ LOG FILE IS PRIVACY COMPLIANT")
        sys.exit(0)
    else:
        print("\n✗ PRIVACY VIOLATIONS DETECTED")
        validator.generate_report()
        sys.exit(1)
