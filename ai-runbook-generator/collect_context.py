#!/usr/bin/env python3
import subprocess
import json
import socket
from datetime import datetime
import os

class SystemContextCollector:
    """Collects system information for runbook generation."""
    
    def __init__(self):
        self.context = {
            "timestamp": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "system_info": {},
            "services": [],
            "network": {},
            "disk": {}
        }
    
    def collect_system_info(self):
        """Collect basic system information."""
        os_release = {}
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if '=' in line:
                        k, v = line.rstrip().split('=', 1)
                        os_release[k] = v.strip('"')
        self.context['system_info']['os_release'] = os_release

        kernel = subprocess.run(['uname', '-r'], capture_output=True, text=True)
        self.context['system_info']['kernel'] = kernel.stdout.strip()

        cpu = subprocess.run(['lscpu'], capture_output=True, text=True)
        self.context['system_info']['cpu_info'] = cpu.stdout[:500]

        mem = subprocess.run(['free', '-h'], capture_output=True, text=True)
        self.context['system_info']['memory'] = mem.stdout
    
    def collect_service_status(self, services):
        """Collect status of specified services."""
        for svc in services:
            active = subprocess.run(['systemctl', 'is-active', svc], capture_output=True, text=True).stdout.strip()
            status = subprocess.run(['systemctl', 'status', svc, '--no-pager'], capture_output=True, text=True).stdout[:300]
            self.context['services'].append({
                "service": svc,
                "active_status": active,
                "details": status
            })
    
    def collect_network_info(self):
        """Collect network configuration."""
        ip_addr = subprocess.run(['ip', 'addr'], capture_output=True, text=True).stdout
        ports = subprocess.run(['ss', '-tulpn'], capture_output=True, text=True).stdout
        self.context['network'] = {
            "interfaces": ip_addr[:1000],
            "listening_ports": ports[:1000]
        }
    
    def collect_disk_info(self):
        """Collect disk usage information."""
        df = subprocess.run(['df', '-h'], capture_output=True, text=True).stdout
        self.context['disk'] = {
            "usage": df
        }
    
    def export_context(self, filename="system_context.json"):
        """Export collected context to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.context, f, indent=2)
        return filename

if __name__ == "__main__":
    collector = SystemContextCollector()
    collector.collect_system_info()
    collector.collect_service_status(['ssh', 'cron'])
    collector.collect_network_info()
    collector.collect_disk_info()
    file_name = collector.export_context()
    print(f"Context collection complete: {file_name}")
