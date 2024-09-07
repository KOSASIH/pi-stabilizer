import unittest
from monitoring.prometheus.prometheus_server import PrometheusServer

class TestPrometheusServer(unittest.TestCase):
    def setUp(self):
        self.config_file = 'path/to/config.json'
        self.port = 8080
        self.server = PrometheusServer(self.config_file, self.port)

    def test_start_server(self):
        self.server.start_server()
        self.assertTrue(self.server.httpd.is_running())

    def test_scrape_metrics(self):
        self.server.scrape_metrics()
        # Verify that metrics are scraped correctly

if __name__ == '__main__':
    unittest.main()
