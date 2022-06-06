FROM debian:stable-slim

# Install Python and pip
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip python3-venv -y

# Update pip and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python3 -m pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

# Copy application files
COPY src/alertmetrics/app.py .
COPY src/alertmetrics/templates/ ./templates/

# Expose port 8080 where the HTTP server serves
EXPOSE 3001

# Start Python HTTP server application
ENTRYPOINT ["poetry", "run", "flask"]
CMD ["run", "--host", "0.0.0.0", "--port", "3001"]
