from abc import ABC, abstractmethod

from ..entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response


class Base64Repository(ABC):
    @abstractmethod
    async def encode(self, request: Base64EncodeRequest) -> Base64Response:
        pass

    @abstractmethod
    async def decode(self, request: Base64DecodeRequest) -> Base64Response:
        pass
