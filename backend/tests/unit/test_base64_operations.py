from unittest.mock import Mock

import pytest

from application.use_cases.base64_operations import Base64UseCases


class TestBase64Operations:
    @pytest.mark.unit
    def test_encode_text_calls_repository(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64UseCases(mock_repository)
        input_text = "test input"
        expected_encoded = "dGVzdCBpbnB1dA=="

        mock_repository.encode.return_value = expected_encoded

        # Act
        result = operations.encode_text(input_text)

        # Assert
        mock_repository.encode.assert_called_once_with(input_text)
        assert result == expected_encoded

    @pytest.mark.unit
    def test_decode_text_calls_repository(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64UseCases(mock_repository)
        encoded_text = "dGVzdCBpbnB1dA=="
        expected_decoded = "test input"

        mock_repository.decode.return_value = expected_decoded

        # Act
        result = operations.decode_text(encoded_text)

        # Assert
        mock_repository.decode.assert_called_once_with(encoded_text)
        assert result == expected_decoded

    @pytest.mark.unit
    def test_encode_text_with_empty_string(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64UseCases(mock_repository)
        input_text = ""
        expected_encoded = ""

        mock_repository.encode.return_value = expected_encoded

        # Act
        result = operations.encode_text(input_text)

        # Assert
        mock_repository.encode.assert_called_once_with(input_text)
        assert result == expected_encoded

    @pytest.mark.unit
    def test_decode_text_with_empty_string(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64UseCases(mock_repository)
        encoded_text = ""
        expected_decoded = ""

        mock_repository.decode.return_value = expected_decoded

        # Act
        result = operations.decode_text(encoded_text)

        # Assert
        mock_repository.decode.assert_called_once_with(encoded_text)
        assert result == expected_decoded
