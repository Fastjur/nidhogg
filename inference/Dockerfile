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

# Copy application files
COPY inference/data/raw/ /data/raw/
COPY inference/data/processed/ /data/processed/
COPY inference/models/ /models/
COPY inference/src/ /src/

RUN python3 src/run.py --preprocess
RUN python3 src/run.py --train

# Expose port 8080 where the HTTP server serves
EXPOSE 8080

# Start Python HTTP server application
ENTRYPOINT ["python3"]
CMD ["src/run.py", "--serve"]
