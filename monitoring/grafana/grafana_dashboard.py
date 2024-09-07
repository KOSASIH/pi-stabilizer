import json

class GrafanaDashboard:
    def __init__(self, dashboard_file):
        self.dashboard_file = dashboard_file
        self.dashboard = self.load_dashboard()

    def load_dashboard(self):
        with open(self.dashboard_file, 'r') as f:
            dashboard = json.load(f)
        return dashboard

    def get_panels(self):
        return self.dashboard.get('panels', [])

    def get_template_variables(self):
        return self.dashboard.get('templating', {}).get('list', [])

    def get_annotations(self):
        return self.dashboard.get('annotations', {}).get('list', [])
