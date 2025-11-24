import pytest

from domain.entities.base64 import Base64DecodeRequest, Base64EncodeRequest


class TestFullFlow:
    @pytest.mark.e2e
    def test_full_flow_via_api(self, client, base64_operations):
        # Arrange
        original_text = "Complete end-to-end test"

        # Act - Encode via API
        encode_response = client.post("/api/v1/tools/encode", json={"text": original_text})
        assert encode_response.status_code == 200
        encoded_text = encode_response.json()["result"]

        # Act - Decode via API
        decode_response = client.post("/api/v1/tools/decode", json={"base64_text": encoded_text})
        assert decode_response.status_code == 200
        decoded_text = decode_response.json()["result"]

        # Assert
        assert decoded_text == original_text

    @pytest.mark.e2e
    def test_full_encode_decode_flow(self, client, base64_operations):
        # Arrange
        original_text = "Complete end-to-end test"

        # Act - Encode via les use cases (pas via API)
        encode_request = Base64EncodeRequest(text=original_text)
        encode_response = base64_operations.encode_text(encode_request)

        # Act - Decode via les use cases
        decode_request = Base64DecodeRequest(base64_text=encode_response.result)
        decode_response = base64_operations.decode_text(decode_request)

        # Assert
        assert decode_response.result == original_text

    @pytest.mark.e2e
    @pytest.mark.slow
    def test_multiple_operations_consistency(self, base64_operations):
        # Arrange
        test_cases = [
            "Simple text",
            "Text with numbers 123",
            "Special characters: @#$%",
            "Unicode: ñáéíóú",
            "Long text " * 10,
        ]

        for original_text in test_cases:
            # Act - Encode via les use cases (pas via API)
            encode_request = Base64EncodeRequest(text=original_text)
            encode_response = base64_operations.encode_text(encode_request)

            # Act - Decode via les use cases
            decode_request = Base64DecodeRequest(base64_text=encode_response.result)
            decode_response = base64_operations.decode_text(decode_request)

            # Assert
            assert decode_response.result == original_text, f"Failed for: {original_text}"
