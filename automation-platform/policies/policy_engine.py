import yaml
import os
from typing import Dict, Any, Tuple

class PolicyEngine:
    """Validates and enforces automation policies."""
    
    def __init__(self, config_path: str = 'config.yaml'):
        if not os.path.exists(config_path):
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            
        self.policy_conf = self.config.get('policies', {})
        self.allowed_types = self.policy_conf.get('allowed_types', ['backup', 'deploy', 'cleanup'])
        self.max_retries = self.policy_conf.get('max_retries', 3)
        self.timeout = self.policy_conf.get('timeout', 300)
    
    def validate_task(self, task_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate task against defined policies."""
        if not isinstance(task_data, dict):
            return False, "Task data must be a dictionary."
            
        task_type = task_data.get('task_type')
        if not task_type:
            return False, "Missing required field: 'task_type'."
            
        if task_type not in self.allowed_types:
            return False, f"Invalid task_type '{task_type}'. Allowed: {self.allowed_types}"
            
        parameters = task_data.get('parameters')
        if parameters is None or not isinstance(parameters, dict):
            return False, "Missing or invalid 'parameters' dictionary."
            
        return True, "Task is valid."
    
    def get_retry_policy(self, task_type: str) -> int:
        """Get retry count for task type."""
        return self.max_retries
