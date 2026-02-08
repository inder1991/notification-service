from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailNotification(BaseModel):
    to: EmailStr
    subject: str
    body: str
    order_id: Optional[str] = None

class SMSNotification(BaseModel):
    phone: str
    message: str

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/email")
async def send_email(notification: EmailNotification):
    logger.info(f"Sending email to {notification.to}: {notification.subject}")
    
    # In production, integrate with email service (SendGrid, AWS SES, etc.)
    # For now, just log it
    logger.info(f"Email content: {notification.body}")
    
    return {
        "success": True,
        "message": f"Email sent to {notification.to}",
        "notification_id": f"EMAIL-{hash(notification.to)}"
    }

@app.post("/sms")
async def send_sms(notification: SMSNotification):
    logger.info(f"Sending SMS to {notification.phone}")
    
    # In production, integrate with SMS service (Twilio, AWS SNS, etc.)
    logger.info(f"SMS content: {notification.message}")
    
    return {
        "success": True,
        "message": f"SMS sent to {notification.phone}",
        "notification_id": f"SMS-{hash(notification.phone)}"
    }

@app.post("/order-confirmation")
async def send_order_confirmation(order_id: str, user_email: EmailStr):
    logger.info(f"Sending order confirmation for {order_id} to {user_email}")
    
    email_body = f"""
    Thank you for your order!
    
    Order ID: {order_id}
    
    Your order has been confirmed and is being processed.
    You will receive another email once your order ships.
    """
    
    return await send_email(EmailNotification(
        to=user_email,
        subject=f"Order Confirmation - {order_id}",
        body=email_body,
        order_id=order_id
    ))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
