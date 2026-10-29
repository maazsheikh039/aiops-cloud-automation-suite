#!/usr/bin/env python3
"""
Dependency-Aware Pipeline Runner
Executes jobs based on their dependencies using topological sorting
"""

import time
import yaml
import subprocess
import sys
from typing import Dict, List, Set, Optional
from enum import Enum
from collections import defaultdict, deque


class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class Job:
    """Represents a single job in the pipeline"""
    
    def __init__(self, name: str, command: str, dependencies: List[str] = None):
        self.name = name
        self.command = command
        self.dependencies = dependencies or []
        self.status = JobStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.error_message = None
    
    def execute(self) -> bool:
        """Execute the job command."""
        self.status = JobStatus.RUNNING
        self.start_time = time.time()
        
        print(f"\n[RUNNING] {self.name}")
        print(f"Command: {self.command}")
        
        try:
            result = subprocess.run(
                self.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.end_time = time.time()
            if result.returncode == 0:
                self.status = JobStatus.SUCCESS
                if result.stdout.strip():
                    print(result.stdout.strip())
                return True
            else:
                self.status = JobStatus.FAILED
                self.error_message = result.stderr.strip() or f"Command exited with code {result.returncode}"
                print(f"[FAILED] {self.name}: {self.error_message}")
                return False
                
        except Exception as e:
            self.end_time = time.time()
            self.status = JobStatus.FAILED
            self.error_message = str(e)
            print(f"[FAILED] {self.name} exception: {self.error_message}")
            return False
    
    def __repr__(self):
        return f"Job({self.name}, status={self.status.value})"


class PipelineRunner:
    """Manages and executes jobs based on dependencies"""
    
    def __init__(self, config_file: str):
        self.jobs: Dict[str, Job] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_graph: Dict[str, List[str]] = defaultdict(list)
        self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """Load pipeline configuration from YAML file."""
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
            
        for job_data in data.get('jobs', []):
            name = job_data['name']
            command = job_data['command']
            deps = job_data.get('dependencies', [])
            
            self.jobs[name] = Job(name, command, deps)
            self.reverse_graph[name] = deps
            for d in deps:
                self.dependency_graph[d].append(name)
    
    def validate_dag(self) -> bool:
        """Validate that the dependency graph is a DAG (no cycles) using DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {job: WHITE for job in self.jobs}
        
        def has_cycle(node: str) -> bool:
            color[node] = GRAY
            for neighbor in self.dependency_graph.get(node, []):
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE:
                    if has_cycle(neighbor):
                        return True
            color[node] = BLACK
            return False
            
        for job in self.jobs:
            if color[job] == WHITE:
                if has_cycle(job):
                    return False
        return True
    
    def topological_sort(self) -> List[str]:
        """Perform topological sort using Kahn's algorithm."""
        in_degree = {job: len(self.reverse_graph[job]) for job in self.jobs}
        queue = deque([job for job, deg in in_degree.items() if deg == 0])
        sorted_order = []
        
        while queue:
            node = queue.popleft()
            sorted_order.append(node)
            
            for dependent in self.dependency_graph.get(node, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
                    
        return sorted_order
    
    def can_execute(self, job_name: str) -> bool:
        """Check if all job dependencies succeeded."""
        deps = self.reverse_graph.get(job_name, [])
        for d in deps:
            if self.jobs[d].status != JobStatus.SUCCESS:
                return False
        return True
    
    def mark_downstream_skipped(self, job_name: str):
        """Recursively mark all downstream dependent jobs as SKIPPED."""
        queue = deque(self.dependency_graph.get(job_name, []))
        visited = set()
        
        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)
            
            job = self.jobs[curr]
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.SKIPPED
                job.error_message = "Skipped due to upstream dependency failure"
                queue.extend(self.dependency_graph.get(curr, []))
    
    def execute_pipeline(self) -> Dict[str, JobStatus]:
        """Execute all jobs in dependency topological order."""
        print("\n" + "="*60)
        print("STARTING PIPELINE EXECUTION")
        print("="*60)
        
        if not self.validate_dag():
            print("ERROR: Cycle detected in dependencies!")
            return {}
            
        execution_order = self.topological_sort()
        print(f"\nExecution order: {' -> '.join(execution_order)}")
        
        for job_name in execution_order:
            job = self.jobs[job_name]
            
            if not self.can_execute(job_name):
                job.status = JobStatus.SKIPPED
                job.error_message = "Skipped due to unsatisfied dependencies"
                print(f"[SKIPPED] {job_name}")
                continue
                
            success = job.execute()
            if not success:
                self.mark_downstream_skipped(job_name)
                
        return {name: job.status for name, job in self.jobs.items()}
    
    def print_summary(self):
        """Print execution summary."""
        print("\n" + "="*60)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*60)
        
        for job_name, job in self.jobs.items():
            duration = ""
            if job.start_time and job.end_time:
                duration = f" ({job.end_time - job.start_time:.2f}s)"
            
            status_symbol = {
                JobStatus.SUCCESS: "✓",
                JobStatus.FAILED: "✗",
                JobStatus.SKIPPED: "⊘",
                JobStatus.PENDING: "○"
            }.get(job.status, "?")
            
            print(f"{status_symbol} {job_name}: {job.status.value}{duration}")
            if job.error_message:
                print(f"  Error: {job.error_message}")
        
        print("="*60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline_runner.py <config_file>")
        sys.exit(1)
        
    config_file = sys.argv[1]
    runner = PipelineRunner(config_file)
    runner.execute_pipeline()
    runner.print_summary()


if __name__ == "__main__":
    main()
