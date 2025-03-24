from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import torch
from chronos import BaseChronosPipeline

app = FastAPI()

# Load the forecasting pipeline at startup.
@app.on_event("startup")
async def startup_event():
    global pipeline
    try:
        pipeline = BaseChronosPipeline.from_pretrained(
            "amazon/chronos-t5-small",  # or "amazon/chronos-bolt-small" if preferred
            device_map="cpu",           # change to "cuda" if GPU is available
            torch_dtype=torch.bfloat16,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load forecasting model: {e}")

# Define the request model.
class ForecastRequest(BaseModel):
    data: list[float]
    prediction_length: int = 3  # default prediction horizon

@app.post("/forecast")
async def get_forecast(request: ForecastRequest):
    data = request.data
    if not data:
        raise HTTPException(status_code=400, detail="Data array cannot be empty")
    
    # Create a DataFrame with a daily datetime index.
    df = pd.DataFrame({'value': data})
    df.index = pd.date_range(start="2024-01-01", periods=len(data), freq='D')
    
    # Convert the 'value' column to a PyTorch tensor.
    context_tensor = torch.tensor(df['value'].values, dtype=torch.float32)
    
    try:
        # Use the provided prediction_length.
        forecast_tensor = pipeline.predict(context_tensor, prediction_length=request.prediction_length)
        # Compute the median along the ensemble dimension.
        median_forecast = torch.median(forecast_tensor, dim=0).values
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")
    
    # Return the forecast as a list.
    return {"forecast": median_forecast.tolist()}
