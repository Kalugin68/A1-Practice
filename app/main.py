from fastapi import FastAPI, UploadFile, Request, APIRouter
from jinja2 import TemplateError

from schemas.email_schema import EmailBroadcastRequest
from schemas.email_schema import EmailRequest
from services.mailer import EmailService
from services.template_service import TemplateService
from schemas.settings import Settings
from contextlib import asynccontextmanager
from routers import email_router, template_router
from services.template_service import TemplateService
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    app.state.template_service = TemplateService()

    app.state.mailer = EmailService(
        host=settings.smtp_host,
        port=settings.smtp_port,
    )

    yield

template_service = TemplateService()
app = FastAPI(lifespan=lifespan)

app.include_router(email_router.router)
app.include_router(template_router.router)

@app.exception_handler(FileNotFoundError)
def file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

@app.exception_handler(ValueError)
def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

@app.get("/")
def root():
    return {"message": "Hello World"}