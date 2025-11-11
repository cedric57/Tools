from src.application.repositories.base64_repository import Base64Repository

from src.domain.entities.base64 import Base64Operation


class Base64RepositoryImpl(Base64Repository):
    def __init__(self):
        self.operations = []

    async def save_operation(self, operation: Base64Operation) -> None:
        self.operations.append(operation)

    async def get_recent_operations(self, limit: int = 10) -> list[Base64Operation]:
        return sorted(self.operations, key=lambda x: x.created_at, reverse=True)[:limit]
