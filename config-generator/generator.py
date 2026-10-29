#!/usr/bin/env python3
"""
Configuration Generator using Jinja2 Templates
"""

import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


class ConfigGenerator:
    """Generate configurations from Jinja2 templates and YAML data."""
    
    def __init__(self, template_dir='templates', output_dir='configs'):
        self.template_dir = template_dir
        self.output_dir = output_dir
        
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def load_data(self, data_file):
        """Load configuration data from YAML file."""
        try:
            with open(data_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading YAML data file {data_file}: {e}")
            sys.exit(1)
    
    def generate_config(self, template_name, data, output_file=None):
        """Generate configuration from template and data."""
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**data)
            
            if output_file is None:
                # Strip .j2 extension for output file name
                output_file = template_name.replace('.j2', '')
                
            out_path = Path(self.output_dir) / output_file
            with open(out_path, 'w') as f:
                f.write(rendered)
                
            print(f"Successfully generated: {out_path}")
            return rendered
        except Exception as e:
            print(f"Error generating config from {template_name}: {e}")
            return None
    
    def generate_all(self, data_file, template_list=None):
        """Generate multiple configurations from a data file."""
        data = self.load_data(data_file)
        
        if template_list is None:
            template_list = [f.name for f in Path(self.template_dir).glob('*.j2')]
            
        for template_name in template_list:
            self.generate_config(template_name, data)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generator.py <data_file> [template1 template2 ...]")
        sys.exit(1)
    
    data_file = sys.argv[1]
    templates = sys.argv[2:] if len(sys.argv) > 2 else None
    
    generator = ConfigGenerator()
    generator.generate_all(data_file, templates)


if __name__ == '__main__':
    main()
