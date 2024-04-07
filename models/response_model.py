from pydantic import BaseModel


class ResponseModel(BaseModel):
    data: dict
