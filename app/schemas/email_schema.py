from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    email: EmailStr
    subject: str = Field(..., min_length=1)
    body: str
    template: str = Field(..., min_length=1)