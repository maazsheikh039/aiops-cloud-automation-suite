#!/usr/bin/env python3
"""
Compliance Report Generator
Generates formatted compliance reports from evidence
"""

import json
import csv
from datetime import datetime
from pathlib import Path

class ComplianceReportGenerator:
    def __init__(self, evidence_data, output_dir='../output'):
        self.evidence_data = evidence_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_json_report(self, filename='compliance_report.json'):
        filepath = self.output_dir / filename
        summary = {}
        for item in self.evidence_data:
            et = item.get('evidence_type', 'unknown')
            summary[et] = summary.get(et, 0) + 1
            
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'report_type': 'compliance_evidence',
                'version': '1.0'
            },
            'evidence_summary': summary,
            'total_evidence_items': len(self.evidence_data),
            'evidence_items': self.evidence_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        return str(filepath)
    
    def generate_html_report(self, filename='compliance_report.html'):
        filepath = self.output_dir / filename
        timestamp = datetime.now().isoformat()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Compliance Evidence Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #2c3e50; color: white; }}
                .summary-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>Compliance Evidence Report</h1>
            <div class="summary-card">
                <p><strong>Generated At:</strong> {timestamp}</p>
                <p><strong>Framework:</strong> NIST 800-53</p>
                <p><strong>Total Evidence Collections:</strong> {len(self.evidence_data)}</p>
            </div>
            <h2>Collected Evidence Details</h2>
        """
        
        for item in self.evidence_data:
            html_content += f"<h3>Type: {item.get('evidence_type')} (Timestamp: {item.get('timestamp')})</h3>"
            html_content += "<pre style='background:#f1f1f1; padding:10px; border-radius:4px;'>"
            html_content += json.dumps(item.get('data'), indent=2)
            html_content += "</pre>"
            
        html_content += """
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return str(filepath)
    
    def generate_csv_report(self, filename='compliance_report.csv'):
        filepath = self.output_dir / filename
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'evidence_type', 'summary_status'])
            for item in self.evidence_data:
                writer.writerow([
                    item.get('timestamp'),
                    item.get('evidence_type'),
                    'SUCCESS'
                ])
        return str(filepath)
