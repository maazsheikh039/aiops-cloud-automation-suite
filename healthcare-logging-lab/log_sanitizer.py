import re
import json
import hashlib
from typing import Dict, Any

class HealthcareLogSanitizer:
    """Sanitizes healthcare logs by masking PII according to HIPAA guidelines."""
    
    def __init__(self):
        self.pii_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ip': r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        }
    
    def mask_ssn(self, ssn: str) -> str:
        """Mask SSN showing only last 4 digits (XXX-XX-1234)."""
        clean_ssn = re.sub(r'\D', '', ssn)
        if len(clean_ssn) == 9:
            return f"XXX-XX-{clean_ssn[5:]}"
        return "XXX-XX-0000"
    
    def mask_email(self, email: str) -> str:
        """Mask email keeping first character and domain (j****@example.com)."""
        if '@' not in email:
            return "masked@example.com"
        username, domain = email.split('@', 1)
        masked_user = username[0] + "****" if len(username) > 0 else "****"
        return f"{masked_user}@{domain}"
    
    def mask_phone(self, phone: str) -> str:
        """Mask phone number showing only last 4 digits (XXX-XXX-1234)."""
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 4:
            return f"XXX-XXX-{digits[-4:]}"
        return "XXX-XXX-0000"
    
    def hash_patient_id(self, patient_id: str) -> str:
        """Create consistent SHA256 hash of patient ID (first 16 chars)."""
        return hashlib.sha256(str(patient_id).encode()).hexdigest()[:16]
    
    def sanitize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize a complete log record dictionary."""
        sanitized = record.copy()
        
        if 'ssn' in sanitized:
            sanitized['ssn'] = self.mask_ssn(str(sanitized['ssn']))
        if 'email' in sanitized:
            sanitized['email'] = self.mask_email(str(sanitized['email']))
        if 'phone' in sanitized:
            sanitized['phone'] = self.mask_phone(str(sanitized['phone']))
        if 'patient_id' in sanitized:
            sanitized['patient_id'] = self.hash_patient_id(str(sanitized['patient_id']))
        if 'name' in sanitized:
            parts = str(sanitized['name']).split()
            if len(parts) >= 2:
                sanitized['name'] = f"{parts[0][0]}. {parts[-1][0]}."
            else:
                sanitized['name'] = "A. B."
        if 'ip_address' in sanitized:
            del sanitized['ip_address']
            
        return sanitized
    
    def process_log_file(self, input_file: str, output_file: str):
        """Process entire log file and create sanitized output."""
        processed = 0
        failed = 0
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    sanitized_rec = self.sanitize_record(record)
                    outfile.write(json.dumps(sanitized_rec) + "\n")
                    processed += 1
                except json.JSONDecodeError:
                    failed += 1
        print(f"Processed {processed} records, Failed {failed} records.")

if __name__ == "__main__":
    sanitizer = HealthcareLogSanitizer()
    sanitizer.process_log_file('healthcare_raw.log', 'healthcare_sanitized.log')
