Getting Started
---------------

This guide provides a step-by-step introduction to getting started with the Pi Stabilizer system.

### Prerequisites

* Raspberry Pi device
* Docker installed on the Raspberry Pi device
* Internet connection

### Step 1: Clone the Repository

* Clone the Pi Stabilizer repository: `git clone https://github.com/KOSASIH/pi-stabilizer.git`

### Step 2: Build the Docker Image

* Build the Docker image: `docker-compose build`

### Step 3: Start the Application

* Start the application: `docker-compose up`

### Step 4: Access the Grafana Dashboard

* Access the Grafana dashboard: `http://localhost:3000`

### Step 5: Access the Prometheus Exporter

* Access the Prometheus exporter: `http://localhost:9090`

### Troubleshooting

* Check the Docker container logs for errors: `docker-compose logs`
* Check the system logs for errors: `sudo journalctl -u pi-stabilizer`
