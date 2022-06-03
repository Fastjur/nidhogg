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
RUN poetry install

# Copy application files and trained models
COPY src/inference.py .
RUN mkdir common
COPY src/common/ ./common/
COPY outputs/nltk_corpora/ .
COPY outputs/models/ .

# Expose port 5000 where the HTTP server serves
EXPOSE 5000

# Start Python HTTP server application
ENTRYPOINT ["poetry", "run", "python3"]
CMD ["inference.py", "./"]
