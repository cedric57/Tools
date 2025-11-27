from pydantic import BaseModel

from domain.value_objects.encoding_types import EncodingTypes


class ToolConfig(BaseModel):
    name: str
    version: str
    supported_encodings: list[str]


class EncodingCategoriesResponse(BaseModel):
    categories: list[dict]

    @classmethod
    def from_domain(cls):
        categories = []
        for category_name, encodings in EncodingTypes.get_encoding_categories():
            categories.append({
                "name": category_name,
                "encodings": [{"value": val, "label": label} for val, label in encodings],
            })
        return cls(categories=categories)


class AnalyticsData(BaseModel):
    total_operations: int = 0
    encode_operations: int = 0
    decode_operations: int = 0
    most_used_encoding: str = "utf-8"
    operations_today: int = 0
