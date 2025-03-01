from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Notification(BaseModel):
    message: str

@app.post("/notify")
async def send_notification(notification: Notification):
    return {"status": "Notification sent", "message": notification.message}
