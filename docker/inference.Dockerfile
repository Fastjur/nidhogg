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

# Copy application files and trained models
COPY src/inference.py .
RUN mkdir common
COPY src/common/ ./common/
COPY outputs/nltk_corpora/ .
COPY outputs/models/ .

ENV FLASK_APP=inference.py

<<<<<<< HEAD
# Expose port 5000 where the HTTP server serves
=======
# Expose port 8080 where the HTTP server serves
>>>>>>> b4cc862c24a4d9dc36e762c291700c101333155e
EXPOSE 8080

# Start Python HTTP server application
ENTRYPOINT ["poetry", "run", "flask"]
CMD ["run", "--host", "0.0.0.0", "--port", "8080"]
