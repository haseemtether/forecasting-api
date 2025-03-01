from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Notification(BaseModel):
    message: str

@app.post("/notify")
async def send_notification(notification: Notification):
    return {"status": "Notification sent", "message": notification.message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)