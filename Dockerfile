# Use a lightweight Python image.
FROM python:3.9-slim

# Install git (needed for installing chronos via pip).
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files.
COPY requirements.txt .

# Upgrade pip and install dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Pre-download the model during build time.
RUN python -c "import torch; from chronos import BaseChronosPipeline; BaseChronosPipeline.from_pretrained('amazon/chronos-t5-base', device_map='cpu', torch_dtype=torch.bfloat16)"

# Copy the application source code.
COPY main.py .

# Expose the port that Uvicorn will run on.
EXPOSE 8000

# Run the FastAPI application with Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
