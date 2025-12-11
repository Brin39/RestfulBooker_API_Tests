import pytest
from logic.auth_api import AuthApi


class TestAuth:
    """Tests for authentication endpoint (T006, T007)."""

    def test_create_token_with_valid_credentials(self):
        """
        T006: Auth - obtain token with valid credentials.
        
        Verifies that valid credentials return a token.
        """
        # Arrange - create API client
        auth_api = AuthApi()
        
        # Act - request token with default (valid) credentials
        response = auth_api.create_token()
        
        # Assert - verify response
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        assert "token" in response_json, (
            f"Expected 'token' in response, got: {response_json}"
        )
        assert response_json["token"], (
            "Token should not be empty"
        )

    def test_create_token_with_invalid_credentials(self):
        """
        T007: Auth - invalid credentials.
        
        Verifies that invalid credentials do not return a token.
        """
        # Arrange - create API client
        auth_api = AuthApi()
        
        # Act - request token with invalid credentials
        response = auth_api.create_token(
            username="invalid_user",
            password="invalid_password"
        )
        
        # Assert - verify response
        # API returns 200 even for bad credentials, but without token
        assert response.status_code in [200, 400, 401, 403], (
            f"Expected status 200/400/401/403, got {response.status_code}"
        )
        
        response_json = response.json()
        assert "token" not in response_json, (
            f"Token should not be present for invalid credentials, got: {response_json}"
        )

