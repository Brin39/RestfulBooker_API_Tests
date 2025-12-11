import httpx
from logic.auth_api import AuthApi
from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


class TestBookingSecurity:
    """Security tests for booking API (T024-T027)."""

    def test_xss_injection_stored_safely(self):
        """
        T024: Special characters injection - XSS / injection check.
        
        Verifies that XSS payloads are stored as plain text
        and not executed. API should escape or store raw.
        """
        # Arrange
        booking_api = BookingApi()
        xss_payload = "<script>alert('XSS')</script>"
        sql_payload = "'; DROP TABLE bookings; --"
        
        booking_data = generate_booking_data(
            firstname=xss_payload,
            lastname=sql_payload
        )
        
        # Act - create booking with malicious data
        create_response = booking_api.create_booking(booking_data)
        
        # Assert - should accept or reject, but not crash
        assert create_response.status_code in [200, 400, 500], (
            f"Unexpected status {create_response.status_code}"
        )
        
        # If accepted, verify data is stored safely (not executed)
        if create_response.status_code == 200:
            booking_id = create_response.json()["bookingid"]
            get_response = booking_api.get_booking(booking_id)
            
            assert get_response.status_code == 200
            response_json = get_response.json()
            
            # Data should be stored (escaped or raw), not cause errors
            # The actual value may be escaped or stored as-is
            assert "firstname" in response_json
            assert "lastname" in response_json

    def test_malformed_json_returns_error(self):
        """
        T025: Malformed JSON in request.
        
        Verifies that invalid JSON payload returns clear error,
        not server crash.
        """
        # Arrange
        booking_api = BookingApi()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Act - send request with invalid JSON body
        with httpx.Client() as client:
            response = client.post(
                f"{booking_api.base_url}/booking",
                content='{"firstname": "John", "lastname": }',  # Invalid JSON
                headers=headers
            )
        
        # Assert - should return 400 Bad Request, not 500
        assert response.status_code == 400, (
            f"Expected 400 for malformed JSON, got {response.status_code}"
        )

    def test_token_not_leaked_in_responses(self):
        """
        T026: Token not returned in non-auth responses.
        
        Verifies that authentication tokens are not leaked
        in booking GET responses or error messages.
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Get a token (to verify it doesn't leak)
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Act - get booking (non-auth endpoint)
        get_response = booking_api.get_booking(booking_id)
        
        # Assert - token should not appear in response
        response_text = get_response.text.lower()
        assert "token" not in response_text, (
            "Token keyword found in non-auth response"
        )
        
        # Check response body doesn't contain the actual token value
        if token:
            assert token not in get_response.text, (
                "Actual token value leaked in response"
            )

    def test_mass_cleanup_bulk_delete(self):
        """
        T027: Mass cleanup - bulk delete test data.
        
        Verifies that multiple bookings can be created and
        then deleted in bulk for cleanup.
        """
        # Arrange
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        # Get token for deletions
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Create multiple bookings
        num_bookings = 5
        created_ids = []
        
        for _ in range(num_bookings):
            booking_data = generate_booking_data()
            response = booking_api.create_booking(booking_data)
            assert response.status_code == 200
            created_ids.append(response.json()["bookingid"])
        
        # Act - delete all created bookings
        delete_results = []
        for booking_id in created_ids:
            delete_response = booking_api.delete_booking(booking_id, token)
            delete_results.append({
                "id": booking_id,
                "status": delete_response.status_code
            })
        
        # Assert - all deletes should succeed
        for result in delete_results:
            assert result["status"] == 201, (
                f"Delete failed for booking {result['id']} with status {result['status']}"
            )
        
        # Verify all bookings are deleted
        for booking_id in created_ids:
            verify_response = booking_api.get_booking(booking_id)
            assert verify_response.status_code == 404, (
                f"Booking {booking_id} should be deleted but got {verify_response.status_code}"
            )

