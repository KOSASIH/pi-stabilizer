import unittest
from monitoring.grafana.grafana_server import GrafanaServer

class TestGrafanaServer(unittest.TestCase):
    def setUp(self):
        self.dashboard_file = 'path/to/dashboard.json'
        self.port = 8081
        self.server = GrafanaServer(self.dashboard_file, self.port)

    def test_start_server(self):
        self.server.start_server()
        self.assertTrue(self.server.httpd.is_running())

    def test_render_dashboard(self):
        self.server.render_dashboard()
        # Verify that dashboard is rendered correctly

if __name__ == '__main__':
    unittest.main()
