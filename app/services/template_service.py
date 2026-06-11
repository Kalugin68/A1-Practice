from pathlib import Path
from fastapi import UploadFile, HTTPException

class TemplateService:
    """Класс, отвечающий за работу с шаблонами"""

    def __init__(self):
        self.templates_dir = Path(__file__).resolve().parent.parent / "templates"

        self.templates_dir.mkdir(exist_ok=True)

    def get_templates(self):
        """Метод, возвращающий список названий шаблонов из директории templates"""

        templates = []

        for file in self.templates_dir.iterdir():
            if file.is_file() and file.suffix == ".html":
                templates.append(file.name)

        return templates

    def save_template(self, file: UploadFile):
        if Path(file.filename).suffix != ".html":
            raise HTTPException(
                status_code=400,
                detail="Файл не соответствует расширению .html"
            )

        template_path = self.templates_dir / file.filename

        content = file.file.read()

        with open(template_path, "wb") as f:
            f.write(content)

        return file.filename