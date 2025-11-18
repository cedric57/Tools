import pytest

from application.repositories.base64_repository import Base64Repository


class TestBase64Repository:
    @pytest.fixture
    def repository(self):
        return Base64Repository()

    @pytest.mark.unit
    def test_encode_should_return_base64_string(self, repository):
        # Arrange
        input_text = "Hello World"
        expected = "SGVsbG8gV29ybGQ="

        # Act
        result = repository.encode(input_text)

        # Assert
        assert result == expected

    @pytest.mark.unit
    def test_encode_empty_string(self, repository):
        # Arrange
        input_text = ""
        expected = ""

        # Act
        result = repository.encode(input_text)

        # Assert
        assert result == expected

    @pytest.mark.unit
    def test_decode_should_return_original_text(self, repository):
        # Arrange
        encoded_text = "SGVsbG8gV29ybGQ="
        expected = "Hello World"

        # Act
        result = repository.decode(encoded_text)

        # Assert
        assert result == expected

    @pytest.mark.unit
    def test_decode_empty_string(self, repository):
        # Arrange
        encoded_text = ""
        expected = ""

        # Act
        result = repository.decode(encoded_text)

        # Assert
        assert result == expected

    @pytest.mark.unit
    def test_encode_decode_roundtrip(self, repository):
        # Arrange
        original_text = "Test roundtrip functionality"

        # Act
        encoded = repository.encode(original_text)
        decoded = repository.decode(encoded)

        # Assert
        assert decoded == original_text

    @pytest.mark.unit
    def test_special_characters(self, repository):
        # Arrange
        special_text = "Hello @World! 123 #$%"

        # Act
        encoded = repository.encode(special_text)
        decoded = repository.decode(encoded)

        # Assert
        assert decoded == special_text
