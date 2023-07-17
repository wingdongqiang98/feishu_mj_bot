# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy Supervisor configuration file
COPY files/feishu_bot_supervisor.conf /etc/supervisor/conf.d/feishu_bot_supervisor.conf

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Supervisor
CMD ["/usr/bin/supervisord"]
