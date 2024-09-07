# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port for Prometheus and Grafana
EXPOSE 9090 3000

# Run the command to start the application
CMD ["python", "main.py"]
