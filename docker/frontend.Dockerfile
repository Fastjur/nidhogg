FROM debian:stable-slim

# Install Python and pip
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip python3-venv -y

# Update pip and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY src/frontend.py .
RUN mkdir frontend
COPY src/templates/ ./templates/

ENV FLASK_APP=frontend.py

# Expose port 8080 where the HTTP server serves
EXPOSE 5000

# Start Python HTTP server application
ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]
