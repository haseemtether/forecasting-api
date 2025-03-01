from fastapi import FastAPI
import requests

app = FastAPI()

# Mock API for fetching weather data
EXTERNAL_API_URL = "https://api.open-meteo.com/v1/forecast?latitude=35&longitude=139&current_weather=true"

@app.get("/ingest")
def ingest_weather_data():
    """Fetches weather data from an external API and returns it."""
    response = requests.get(EXTERNAL_API_URL)
    if response.status_code == 200:
        return {"status": "success", "data": response.json()}
    return {"status": "error", "message": "Failed to fetch weather data"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
