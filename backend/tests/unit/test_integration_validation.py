from application.repositories.base64_repository import Base64Repository
from application.use_cases.base64_operations import Base64Operations
from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest


class TestIntegrationValidation:
    """Tests pour valider l'intégration réelle entre use cases et repository"""

    def test_real_encode_decode_flow(self):
        # Arrange
        repository = Base64Repository()
        operations = Base64Operations(repository)

        original_text = "Hello World"
        input_request = Base64EncodeRequest(text=original_text)

        # Act
        encoded = operations.encode_text(input_request)

        # Act - Decode via les use cases
        decode_request = Base64DecodeRequest(base64_text=encoded.result)
        decoded = operations.decode_text(decode_request)

        # Assert
        assert decoded.result == original_text
        assert encoded.result == "SGVsbG8gV29ybGQ="

    def test_real_encode_decode_empty_string(self):
        # Arrange
        repository = Base64Repository()
        operations = Base64Operations(repository)

        original_text = ""
        input_request = Base64EncodeRequest(text=original_text)

        # Act
        encoded = operations.encode_text(input_request)

        # Act - Decode via les use cases
        decode_request = Base64DecodeRequest(base64_text=encoded.result)
        decoded = operations.decode_text(decode_request)

        # Assert
        assert decoded.result == original_text
        assert encoded.result == ""
