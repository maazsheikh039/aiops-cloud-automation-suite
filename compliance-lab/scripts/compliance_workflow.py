#!/usr/bin/env python3
"""
Main Compliance Workflow Orchestrator
Coordinates evidence collection, reporting, and audit logging
"""

import sys
from pathlib import Path
from evidence_collector import EvidenceCollector
from report_generator import ComplianceReportGenerator
from audit_logger import AuditLogger

class ComplianceWorkflow:
    def __init__(self, config_path):
        self.config_path = config_path
        self.collector = EvidenceCollector(config_path)
        self.audit_logger = AuditLogger()
    
    def run_full_compliance_cycle(self):
        results = {
            'evidence_collected': [],
            'reports_generated': [],
            'errors': []
        }
        
        try:
            # Step 1: Collect Evidence
            for ev_type in ['system_logs', 'access_logs', 'configuration_snapshots']:
                try:
                    if ev_type == 'system_logs':
                        ev = self.collector.collect_system_logs()
                    elif ev_type == 'access_logs':
                        ev = self.collector.collect_access_logs()
                    else:
                        ev = self.collector.collect_configuration_snapshot()
                        
                    results['evidence_collected'].append(ev)
                    self.audit_logger.log_evidence_collection(ev_type, 'SUCCESS', {'items_count': len(ev.get('data', {}))})
                except Exception as e:
                    results['errors'].append(str(e))
                    self.audit_logger.log_evidence_collection(ev_type, 'FAILED', {'error': str(e)})
            
            # Step 2: Generate Reports
            generator = ComplianceReportGenerator(results['evidence_collected'])
            
            json_path = generator.generate_json_report()
            results['reports_generated'].append(json_path)
            self.audit_logger.log_report_generation('json', json_path, 'SUCCESS')
            
            html_path = generator.generate_html_report()
            results['reports_generated'].append(html_path)
            self.audit_logger.log_report_generation('html', html_path, 'SUCCESS')
            
            csv_path = generator.generate_csv_report()
            results['reports_generated'].append(csv_path)
            self.audit_logger.log_report_generation('csv', csv_path, 'SUCCESS')
            
        except Exception as e:
            results['errors'].append(str(e))
            
        return results
    
    def display_summary(self, results):
        print("\n" + "="*50)
        print("COMPLIANCE WORKFLOW EXECUTION SUMMARY")
        print("="*50)
        print(f"Evidence Types Collected: {len(results['evidence_collected'])}")
        print(f"Reports Generated: {len(results['reports_generated'])}")
        print(f"Errors Encountered: {len(results['errors'])}")
        if results['errors']:
            print("Errors:", results['errors'])
        print("="*50)

def main():
    config_path = '../config/compliance_config.yaml'
    workflow = ComplianceWorkflow(config_path)
    results = workflow.run_full_compliance_cycle()
    workflow.display_summary(results)
    
    print("\nCompliance workflow completed!")
    print("Check the following directories:")
    print("  - output/ for generated reports")
    print("  - logs/ for audit logs")

if __name__ == "__main__":
    main()
