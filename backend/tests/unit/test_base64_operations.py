import pytest

from application.repositories.base64_repository import Base64Repository
from application.use_cases.base64_operations import Base64Operations
from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response


class TestBase64Operations:
    @pytest.fixture
    def operations(self):
        repository = Base64Repository()
        return Base64Operations(repository)

    @pytest.mark.unit
    def test_encode_text_integration(self, operations):
        # Arrange
        input_request = Base64EncodeRequest(text="test input")

        # Act
        encoded = operations.encode_text(input_request)

        # Assert
        assert isinstance(encoded, Base64Response)
        assert encoded.result == "dGVzdCBpbnB1dA=="

    @pytest.mark.unit
    def test_decode_text_integration(self, operations):
        # Arrange
        input_request = Base64DecodeRequest(base64_text="dGVzdCBpbnB1dA==")

        # Act
        decoded = operations.decode_text(input_request)

        # Assert
        assert isinstance(decoded, Base64Response)
        assert decoded.result == "test input"
