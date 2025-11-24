from unittest.mock import Mock

import pytest

from application.use_cases.base64_operations import Base64Operations
from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest, Base64Response


class TestBase64Operations:
    @pytest.mark.unit
    def test_encode_text_calls_repository(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64Operations(mock_repository)

        original_text = "test input"
        input_request = Base64EncodeRequest(text=original_text)
        expected_encoded = "dGVzdCBpbnB1dA=="

        # Configurer le mock pour retourner une valeur
        mock_repository.encode_text.return_value = expected_encoded

        # Act
        result = operations.encode_text(input_request)

        # Debug: voir ce qui est vraiment appelé
        print(f"Mock calls: {mock_repository.method_calls}")
        print(f"Mock encode calls: {mock_repository.encode_text.call_args_list}")

        # Assert
        mock_repository.encode_text.assert_called_once_with(original_text)
        assert isinstance(result, Base64Response)
        assert result == expected_encoded

    @pytest.mark.unit
    def test_decode_text_calls_repository(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64Operations(mock_repository)

        encoded_text = "dGVzdCBpbnB1dA=="
        input_request = Base64DecodeRequest(base64_text=encoded_text)
        expected_decoded = "test input"

        mock_repository.decode_text.return_value = expected_decoded

        # Act
        result = operations.decode_text(input_request)

        # Assert
        mock_repository.decode_text.assert_called_once_with(encoded_text)
        assert result == expected_decoded

    @pytest.mark.unit
    def test_encode_text_with_empty_string(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64Operations(mock_repository)

        input_request = Base64EncodeRequest(text="")
        expected_encoded = ""

        mock_repository.encode.return_value = expected_encoded

        # Act
        result = operations.encode_text(input_request)

        # Assert
        mock_repository.encode.assert_called_once_with("")
        assert result == expected_encoded

    @pytest.mark.unit
    def test_decode_text_with_empty_string(self):
        # Arrange
        mock_repository = Mock()
        operations = Base64Operations(mock_repository)

        input_request = Base64DecodeRequest(base64_text="")
        expected_decoded = ""

        mock_repository.decode.return_value = expected_decoded

        # Act
        result = operations.decode_text(input_request)

        # Assert
        mock_repository.decode.assert_called_once_with("")
        assert result == expected_decoded
