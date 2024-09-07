import http.server
import socketserver

class GrafanaServer:
    def __init__(self, dashboard_file, port):
        self.dashboard_file = dashboard_file
        self.port = port
        self.dashboard = GrafanaDashboard(dashboard_file)

    def start_server(self):
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            print(f"Grafana server started on port {self.port}")
            httpd.serve_forever()

    def render_dashboard(self):
        # Render the dashboard
        panels = self.dashboard.get_panels()
        template_variables = self.dashboard.get_template_variables()
        annotations = self.dashboard.get_annotations()
        print(f"Rendering dashboard with {len(panels)} panels, {len(template_variables)} template variables, and {len(annotations)} annotations")

    def run(self):
        self.start_server()
        self.render_dashboard()
