import os
import json

class PrometheusConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        return config

    def get_scrape_configs(self):
        return self.config.get('scrape_configs', [])

    def get_alertmanager_config(self):
        return self.config.get('alertmanager', {})

    def get_rule_files(self):
        return self.config.get('rule_files', [])

    def get_global_config(self):
        return self.config.get('global', {})
