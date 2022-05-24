FROM debian:stable-slim

# Install Python and pip
RUN apt-get update && apt-get upgrade -y
RUN apt install python3-pip python3-venv -y

# Update pip and install Python dependencies
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application files and trained models
COPY src/inference_api.py .
RUN mkdir common
COPY src/common/ ./common/
COPY outputs/models/vectorizer.pkl .
COPY outputs/models/tfidf_model.pkl .

# Expose port 8080 where the HTTP server serves
EXPOSE 8080

# Start Python HTTP server application
ENTRYPOINT ["python3"]
CMD ["inference_api.py"]
