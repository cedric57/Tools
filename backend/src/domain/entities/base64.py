from datetime import datetime

from pydantic import BaseModel


class Base64Operation(BaseModel):
    id: str | None = None
    input_data: str
    output_data: str
    operation_type: str  # 'encode' or 'decode'
    encoding: str
    line_by_line: bool = False
    created_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.utcnow()


class Base64EncodeRequest(BaseModel):
    text: str
    charset: str = "utf-8"


class Base64DecodeRequest(BaseModel):
    base64_text: str
    charset: str = "utf-8"
    decode_line_by_line: bool = False


class Base64Response(BaseModel):
    success: bool
    result: str | None = None
    error: str | None = None
    original_input: str | None = None
    encoding_used: str | None = None
    operation_id: str | None = None
