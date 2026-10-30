#!/usr/bin/env python3
import os
import json
from typing import Optional, List
from datetime import datetime

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.profiles_dir = os.path.join(config_dir, "profiles")
        self.current_config_file = os.path.join(config_dir, "active_profile.json")
        os.makedirs(config_dir, exist_ok=True)
    
    def set_active_profile(self, profile_name: str) -> None:
        data = {
            "profile": profile_name,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.current_config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def get_active_profile(self) -> Optional[str]:
        if not os.path.exists(self.current_config_file):
            return None
        try:
            with open(self.current_config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("profile")
        except Exception:
            return None
    
    def list_available_profiles(self) -> List[str]:
        if not os.path.exists(self.profiles_dir):
            return []
        profiles = []
        for file in os.listdir(self.profiles_dir):
            if file.endswith('.yaml') or file.endswith('.yml'):
                profiles.append(os.path.splitext(file)[0])
        return sorted(profiles)
