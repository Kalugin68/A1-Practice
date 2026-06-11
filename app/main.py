from fastapi import FastAPI, UploadFile
from schemas.email_schema import EmailRequest
from services.mailer import EmailService
from services.template_service import TemplateService

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

@app.get("/templates")
def get_templates():
    """Маршрут получения названий всех html-файлов"""

    return {"templates": TemplateService().get_templates()}

@app.post("/templates")
def post_template(file: UploadFile):
    """Маршрут отправки html-файла"""

    return {"message": "Файл успешно сохранён",
            "filename": TemplateService().save_template(file)}

@app.get("/")
def root():
    return {"message": "Hello World"}