from fastapi import APIRouter, Request
from schemas.email_schema import EmailRequest, EmailBroadcastRequest


router = APIRouter(prefix="/emails", tags=["email"])

@router.post("/send")
def send_email(data: EmailRequest, request: Request):
    """Маршрут отправки сообщения"""

    template_content = request.app.state.template_service.render_template(data.template, data.context)

    request.app.state.mailer.send_email(
        data.email, data.subject, template_content)

    return {"email": data.email,
            "subject": data.subject,
            "template": template_content,
            "context": data.context}

@router.post("/broadcast")
def send_broadcast(data:EmailBroadcastRequest, request: Request):
    """Маршрут отправки широковещательного сообщения"""

    for email, user_context in data.emails.items():
        template_content = request.app.state.template_service.render_template(data.template, user_context)

        request.app.state.mailer.send_email(email, data.subject, template_content)

    return {"sent": len(data.emails)}