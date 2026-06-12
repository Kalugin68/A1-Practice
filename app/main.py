from fastapi import FastAPI, UploadFile, Request
from schemas.email_schema import EmailBroadcastRequest
from schemas.email_schema import EmailRequest
from services.mailer import EmailService
from services.template_service import TemplateService
from schemas.settings import Settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    app.state.template_service = TemplateService()

    app.state.mailer = EmailService(
        host=settings.smtp_host,
        port=settings.smtp_port,
    )

    yield

app = FastAPI(lifespan=lifespan)

@app.post("/send")
def send_email(data: EmailRequest, request: Request):
    """Маршрут отправки сообщения"""

    template_content = request.app.state.template_service.render_template(data.template, data.context)

    request.app.state.mailer.send_email(
        data.email, data.subject, template_content)

    return {"email": data.email,
            "subject": data.subject,
            "template": template_content,
            "context": data.context}

@app.post("/broadcast")
def send_broadcast(data:EmailBroadcastRequest, request: Request):
    """Маршрут отправки широковещательного сообщения"""

    for email, user_context in data.emails.items():
        template_content = request.app.state.template_service.render_template(data.template, user_context)

        request.app.state.mailer.send_email(email, data.subject, template_content)

    return {"sent": len(data.emails)}

@app.get("/templates")
def get_templates(request: Request):
    """Маршрут получения названий всех html-файлов"""

    return {"templates": request.app.state.template_service.get_templates()}

@app.post("/templates")
def post_template(file: UploadFile, request: Request):
    """Маршрут отправки html-файла"""

    return {"message": "Файл успешно сохранён",
            "filename": request.app.state.template_service.save_template(file)}

@app.get("/")
def root():
    return {"message": "Hello World"}