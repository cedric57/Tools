from pydantic import BaseModel


class SEOConfig(BaseModel):
    title: str
    description: str
    keywords: str
    canonical_url: str
    og_title: str
    og_description: str
    og_image: str = "/static/images/og-image.jpg"


class EncodingCategory(BaseModel):
    name: str
    encodings: list[tuple[str, str]]


class PageContext(BaseModel):
    seo: SEOConfig
    decoded_result: str = ""
    encoded_result: str = ""
    decode_error: str = ""
    encode_error: str = ""
    original_base64: str = ""
    original_text: str = ""
    charset: str = "utf-8"
    encoding_categories: list[EncodingCategory] = []
