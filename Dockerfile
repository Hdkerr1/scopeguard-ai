FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Port that Streamlit will run on. Vercel will set PORT env var at runtime.
ENV PORT 8080
EXPOSE 8080

CMD ["bash", "-lc", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]
