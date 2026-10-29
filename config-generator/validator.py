#!/usr/bin/env python3
"""
Configuration Validator using JSON Schema
"""

import sys
import yaml
import json
from jsonschema import validate, ValidationError
from pathlib import Path


class ConfigValidator:
    """Validate generated configurations against schemas."""
    
    def __init__(self, schema_dir='schemas'):
        self.schema_dir = schema_dir
        self.schemas = {}
    
    def load_schema(self, schema_name):
        """Load a JSON schema file."""
        if schema_name in self.schemas:
            return self.schemas[schema_name]
            
        schema_path = Path(self.schema_dir) / schema_name
        try:
            with open(schema_path, 'r') as f:
                schema = json.load(f)
                self.schemas[schema_name] = schema
                return schema
        except Exception as e:
            print(f"Error loading schema {schema_name}: {e}")
            sys.exit(1)
    
    def validate_yaml_config(self, config_file, schema_name):
        """Validate a YAML configuration file against a schema."""
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
                
            schema = self.load_schema(schema_name)
            validate(instance=config_data, schema=schema)
            return True, []
        except ValidationError as e:
            return False, [e.message]
        except Exception as e:
            return False, [str(e)]
    
    def validate_nginx_config(self, config_file):
        """Perform basic syntax validation on Nginx config."""
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                
            # Check for balanced braces
            if content.count('{') != content.count('}'):
                return False, "Unbalanced curly braces in Nginx configuration"
                
            if 'server {' not in content:
                return False, "Missing 'server' block in Nginx configuration"
                
            return True, "Nginx configuration syntax check passed"
        except Exception as e:
            return False, str(e)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 validator.py <config_file> <schema_name>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    schema_name = sys.argv[2]
    
    validator = ConfigValidator()
    
    if schema_name == 'nginx':
        is_valid, msg = validator.validate_nginx_config(config_file)
    else:
        is_valid, errors = validator.validate_yaml_config(config_file, schema_name)
        msg = "Validation passed" if is_valid else f"Validation errors: {errors}"
        
    print(msg)
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
