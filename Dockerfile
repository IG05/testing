FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy code into image
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -c "from transformers import CLIPProcessor, pipeline; \
    CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32'); \
    pipeline('automatic-speech-recognition', model='openai/whisper-small.en')"


# Expose port for FastAPI
ENV PORT=7000
EXPOSE 7000

# Start server
CMD ["python", "main.py"]
