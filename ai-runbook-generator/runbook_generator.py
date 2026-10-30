#!/usr/bin/env python3
import json
import requests
import yaml
from jinja2 import Template
from datetime import datetime

class RunbookGenerator:
    """Generates operational runbooks using AI assistance."""
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama3.2:1b"
    
    def load_context(self, context_file):
        """Load system context from JSON file."""
        with open(context_file, 'r') as f:
            return json.load(f)
    
    def create_prompt(self, context, scenario):
        """Create AI prompt for runbook generation."""
        prompt = f"""
You are an expert Senior Site Reliability Engineer. Generate a structured, professional incident remediation runbook based on the following system context and incident scenario.

INCIDENT SCENARIO:
{scenario}

SYSTEM CONTEXT SUMMARY:
- Hostname: {context.get('hostname')}
- OS: {context.get('system_info', {}).get('os_release', {}).get('PRETTY_NAME', 'Linux')}
- Kernel: {context.get('system_info', {}).get('kernel', 'Unknown')}
- Disk Usage: {context.get('disk', {}).get('usage', 'N/A')}

Provide the output with the following sections clearly marked:
1. Title
2. Prerequisites (bullet points)
3. Procedure (numbered step-by-step shell or troubleshooting commands)
4. Verification Steps
5. Rollback Procedure
"""
        return prompt.strip()
    
    def generate_with_ai(self, prompt):
        """Call Ollama API to generate runbook content."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Error: No response field in AI output.")
        except Exception as e:
            return f"Error connecting to Ollama service: {str(e)}"
    
    def format_runbook(self, ai_output, context, scenario):
        """Format AI output into structured runbook dictionary."""
        runbook = {
            "title": f"Incident Response Runbook: {scenario.title()}",
            "created": datetime.now().isoformat(),
            "hostname": context.get("hostname", "unknown"),
            "os_version": context.get("system_info", {}).get("os_release", {}).get("PRETTY_NAME", "Linux"),
            "kernel": context.get("system_info", {}).get("kernel", "unknown"),
            "memory": "Checked via system collector",
            "scenario": scenario,
            "prerequisites": "Root access / sudo privileges, SSH access, monitoring tool permissions.",
            "procedure": ai_output,
            "verification": "Run health checks, verify service responsiveness and CPU/disk metrics.",
            "rollback": "Revert configuration changes, restart affected services, or restore from snapshot if failure persists."
        }
        return runbook
    
    def export_runbook(self, runbook, scenario_name):
        """Export runbook to Markdown and YAML files."""
        try:
            with open("runbook_template.md", "r") as f:
                template_content = f.read()
            template = Template(template_content)
            md_output = template.render(runbook)
            
            md_filename = f"runbook_{scenario_name}.md"
            with open(md_filename, "w") as f:
                f.write(md_output)
            print(f"Exported Markdown runbook to {md_filename}")
        except Exception as e:
            print(f"Error rendering markdown template: {e}")

        yaml_filename = f"runbook_{scenario_name}.yaml"
        with open(yaml_filename, "w") as f:
            yaml.dump(runbook, f, default_flow_style=False)
        print(f"Exported YAML runbook to {yaml_filename}")
