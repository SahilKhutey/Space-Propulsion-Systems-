FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY services/simulation_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to root so 'core' and 'engines' can be imported absolutely
ENV PYTHONPATH=/workspace

COPY . .

EXPOSE 8000

CMD ["uvicorn", "services.simulation_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
