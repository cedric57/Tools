from pydantic import BaseModel


class Base64EncodeRequest(BaseModel):
    text: str
    charset: str = "utf-8"


class Base64DecodeRequest(BaseModel):
    base64_text: str
    charset: str = "utf-8"


class Base64Response(BaseModel):
    success: bool
    result: str | None = None
    error: str | None = None
    original_input: str | None = None
