from ...core.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response
from ...core.ports.base64_repository import Base64Repository


class Base64UseCases:
    def __init__(self, repository: Base64Repository):
        self.repository = repository

    async def encode_text(self, request: Base64EncodeRequest) -> Base64Response:
        return await self.repository.encode(request)

    async def decode_text(self, request: Base64DecodeRequest) -> Base64Response:
        return await self.repository.decode(request)
