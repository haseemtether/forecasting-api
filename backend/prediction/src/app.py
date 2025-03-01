from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PredictionInput(BaseModel):
    temperature: float
    wind_speed: float
    humidity: float

@app.post("/predict")
def predict(data: PredictionInput):
    """Dummy weather prediction based on input data."""
    if data.temperature > 30:
        forecast = "Sunny"
    elif data.humidity > 70:
        forecast = "Rainy"
    else:
        forecast = "Cloudy"
    
    return {"prediction": forecast, "confidence": "80%"}
