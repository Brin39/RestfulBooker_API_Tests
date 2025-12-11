from logic.ping_api import PingApi


class TestPing:
    """Tests for API health check endpoint (T018)."""

    def test_health_check_returns_success_status(self):
        """
        T018: Ping/health - service availability.
        
        Verifies that the API service is running and accessible
        by checking the /ping endpoint returns expected status.
        """
        # Arrange - create API client
        ping_api = PingApi()
        
        # Act - perform health check
        response = ping_api.health_check()
        
        # Assert - verify response
        assert response.status_code == 201, (
            f"Expected status 201, got {response.status_code}"
        )
        assert "Created" in response.text, (
            f"Expected 'Created' in response, got: {response.text}"
        )

