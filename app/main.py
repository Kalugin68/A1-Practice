from fastapi import FastAPI
from schemas import EmailRequest
from services.mailer import EmailService
app = FastAPI()

@app.post("/send")
def send_email(data: EmailRequest):
    """Маршрут отправки сообщения"""

    # Создание экземпляра класса и вызов метода
    EmailService(host="mailpit", port=1025).send_email(
        data.email, data.subject, data.body)

    return {"email": data.email,
            "subject": data.subject,
            "body": data.body}

@app.get("/")
def root():
    return {"message": "Hello World"}