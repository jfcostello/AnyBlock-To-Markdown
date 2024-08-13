import yaml
import os

class Config:
    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    def get(self, key, default=None):
        return self.config.get(key, default)

config = Config()