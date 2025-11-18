import pytest


class TestBase64API:
    @pytest.mark.integration
    def test_encode_endpoint_success(self, client):
        # Arrange
        request_data = {"text": "Hello API"}

        # Act
        response = client.post("/encode", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "encoded" in data
        assert data["encoded"] == "SGVsbG8gQVBJ"

    @pytest.mark.integration
    def test_decode_endpoint_success(self, client):
        # Arrange
        request_data = {"encoded": "SGVsbG8gQVBJ"}

        # Act
        response = client.post("/decode", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "decoded" in data
        assert data["decoded"] == "Hello API"

    @pytest.mark.integration
    def test_encode_endpoint_missing_field(self, client):
        # Arrange
        request_data = {"wrong_field": "test"}

        # Act
        response = client.post("/encode", json=request_data)

        # Assert
        assert response.status_code == 422  # Validation error

    @pytest.mark.integration
    def test_decode_endpoint_missing_field(self, client):
        # Arrange
        request_data = {"wrong_field": "test"}

        # Act
        response = client.post("/decode", json=request_data)

        # Assert
        assert response.status_code == 422  # Validation error

    @pytest.mark.integration
    def test_encode_endpoint_empty_string(self, client):
        # Arrange
        request_data = {"text": ""}

        # Act
        response = client.post("/encode", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["encoded"] == ""

    @pytest.mark.integration
    def test_decode_endpoint_empty_string(self, client):
        # Arrange
        request_data = {"encoded": ""}

        # Act
        response = client.post("/decode", json=request_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["decoded"] == ""

    @pytest.mark.integration
    def test_health_check_endpoint(self, client):
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
