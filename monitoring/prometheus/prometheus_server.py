import http.server
import socketserver

class PrometheusServer:
    def __init__(self, config_file, port):
        self.config_file = config_file
        self.port = port
        self.config = PrometheusConfig(config_file)

    def start_server(self):
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), Handler) as httpd:
            print(f"Prometheus server started on port {self.port}")
            httpd.serve_forever()

    def scrape_metrics(self):
        # Scrape metrics from targets
        for scrape_config in self.config.get_scrape_configs():
            target = scrape_config['targets'][0]
            print(f"Scraping metrics from {target}")
            # Simulated metric scraping
            metrics = {'metric1': 10, 'metric2': 20}
            print(f"Metrics: {metrics}")

    def run(self):
        self.start_server()
        self.scrape_metrics()
