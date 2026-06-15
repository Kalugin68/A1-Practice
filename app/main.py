from fastapi import FastAPI, UploadFile, Request, APIRouter
from schemas.email_schema import EmailBroadcastRequest
from schemas.email_schema import EmailRequest
from services.mailer import EmailService
from services.template_service import TemplateService
from schemas.settings import Settings
from contextlib import asynccontextmanager
from routers import email_router, template_router


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

app.include_router(email_router.router)
app.include_router(template_router.router)

@app.get("/")
def root():
    return {"message": "Hello World"}