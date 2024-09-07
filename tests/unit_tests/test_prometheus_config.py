import unittest
from monitoring.prometheus.prometheus_config import PrometheusConfig

class TestPrometheusConfig(unittest.TestCase):
    def setUp(self):
        self.config_file = 'path/to/config.json'
        self.config = PrometheusConfig(self.config_file)

    def test_load_config(self):
        self.assertIsNotNone(self.config.config)

    def test_get_scrape_configs(self):
        scrape_configs = self.config.get_scrape_configs()
        self.assertIsInstance(scrape_configs, list)

    def test_get_alertmanager_config(self):
        alertmanager_config = self.config.get_alertmanager_config()
        self.assertIsInstance(alertmanager_config, dict)

    def test_get_rule_files(self):
        rule_files = self.config.get_rule_files()
        self.assertIsInstance(rule_files, list)

    def test_get_global_config(self):
        global_config = self.config.get_global_config()
        self.assertIsInstance(global_config, dict)

if __name__ == '__main__':
    unittest.main()
