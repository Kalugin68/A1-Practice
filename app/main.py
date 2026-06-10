import smtplib
from fastapi import FastAPI
from email.message import EmailMessage
from schemas import EmailRequest

app = FastAPI()

@app.post("/send")
def send_email(data: EmailRequest):
    msg = EmailMessage()

    msg["Subject"] = "Test message"
    msg["From"] = "sashakalugin74@gmail.com"
    msg["To"] = data.email

    msg.set_content(data.body)

    with smtplib.SMTP("mailpit", 1025) as smtp:
        smtp.send_message(msg)

    return {"message": "Email sent successfully",
            "email": data.email,
            "body": data.body}

@app.get("/")
def root():
    return {"message": "Hello World"}