from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class WeatherData(BaseModel):
    temperature: float
    wind_speed: float
    humidity: float

@app.post("/process")
def process_weather_data(data: WeatherData):
    """
    Processes raw weather data and returns a structured format.
    """
    processed_data = {
        "temperature_celsius": round(data.temperature, 2),
        "wind_speed_kmh": round(data.wind_speed * 3.6, 2),  # Convert m/s to km/h
        "humidity": data.humidity
    }
    
    return {"status": "success", "processed_data": processed_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
