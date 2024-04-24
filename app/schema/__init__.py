from pydantic import BaseModel


class BasicResponse(BaseModel):
    response_code: str = "200"
    response_message: str = "OK"
