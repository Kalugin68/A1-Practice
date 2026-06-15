from fastapi import APIRouter, Request, HTTPException

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/liveness")
def liveness():
    """Проверка, работает ли приложение"""

    return {"message": "OK"}

@router.get("/readiness")
def readiness(request: Request):
    """Проверка, готов ли работать Mailpit"""

    request.app.state.mailer.healthcheck()

    return {"message": "OK"}
