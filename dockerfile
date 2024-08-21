# app/Dockerfile
 
FROM python:3.9-slim
 
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libasound2 \
    libasound2-dev \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

COPY . .
 
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
 
RUN mkdir tmp
 
EXPOSE 8501
 
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
 
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]