from pydantic import BaseModel


class ComplaintCreateDTO(BaseModel):
    text: str
