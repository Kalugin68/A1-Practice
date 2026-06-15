from fastapi import APIRouter, Request, UploadFile


router = APIRouter(prefix="/templates", tags=["template"])

@router.get("/")
def get_templates(request: Request):
    """Маршрут получения названий всех html-файлов"""

    return {"templates": request.app.state.template_service.get_templates()}

@router.post("/")
def post_template(file: UploadFile, request: Request):
    """Маршрут отправки html-файла"""

    return {"message": "Файл успешно сохранён",
            "filename": request.app.state.template_service.save_template(file)}
