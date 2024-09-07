import unittest
from monitoring.grafana.grafana_dashboard import GrafanaDashboard

class TestGrafanaDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard_file = 'path/to/dashboard.json'
        self.dashboard = GrafanaDashboard(self.dashboard_file)

    def test_load_dashboard(self):
        self.assertIsNotNone(self.dashboard.dashboard)

    def test_get_panels(self):
        panels = self.dashboard.get_panels()
        self.assertIsInstance(panels, list)

    def test_get_template_variables(self):
        template_variables = self.dashboard.get_template_variables()
        self.assertIsInstance(template_variables, list)

    def test_get_annotations(self):
        annotations = self.dashboard.get_annotations()
        self.assertIsInstance(annotations, list)

if __name__ == '__main__':
    unittest.main()
