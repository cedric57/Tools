from application.repositories.base64_repository import Base64Repository
from application.use_cases.base64_operations import Base64Operations


class TestIntegrationValidation:
    """Tests pour valider l'intégration réelle entre use cases et repository"""

    def test_real_encode_decode_flow(self):
        # Arrange
        repository = Base64Repository()
        operations = Base64Operations(repository)
        original_text = "Hello World"

        # Act
        encoded = operations.encode_text(original_text)
        decoded = operations.decode_text(encoded)

        # Assert
        assert decoded == original_text
        assert encoded == "SGVsbG8gV29ybGQ="

    def test_real_encode_decode_empty_string(self):
        # Arrange
        repository = Base64Repository()
        operations = Base64Operations(repository)
        original_text = ""

        # Act
        encoded = operations.encode_text(original_text)
        decoded = operations.decode_text(encoded)

        # Assert
        assert decoded == original_text
        assert encoded == ""
