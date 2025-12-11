from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


class TestBookingNegative:
    """Negative tests for booking API (T008-T015)."""

    def test_update_booking_without_token(self):
        """
        T008: Update without token - access denied.
        
        Verifies that PUT without authentication returns 401/403.
        """
        # Arrange - create a booking (no token needed for create)
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Prepare update data
        updated_data = generate_booking_data()
        
        # Act - try to update WITHOUT token
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = booking_api.send_request(
            "PUT",
            f"/booking/{booking_id}",
            payload=updated_data,
            headers=headers
        )
        
        # Assert - should be forbidden
        assert response.status_code in [401, 403], (
            f"Expected status 401 or 403, got {response.status_code}"
        )

    def test_delete_booking_without_token(self):
        """
        T009: Delete without token - access denied.
        
        Verifies that DELETE without authentication returns 401/403.
        """
        # Arrange - create a booking
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Act - try to delete WITHOUT token
        headers = {
            "Content-Type": "application/json"
        }
        response = booking_api.send_request(
            "DELETE",
            f"/booking/{booking_id}",
            headers=headers
        )
        
        # Assert - should be forbidden
        assert response.status_code in [401, 403], (
            f"Expected status 401 or 403, got {response.status_code}"
        )
        
        # Verify booking still exists
        get_response = booking_api.get_booking(booking_id)
        assert get_response.status_code == 200, (
            "Booking should still exist after failed delete"
        )

    def test_create_booking_empty_required_fields(self):
        """
        T010: Create booking - empty required fields.
        
        Verifies that POST with empty firstname/lastname is handled.
        """
        # Arrange
        booking_api = BookingApi()
        invalid_data = generate_booking_data(firstname="", lastname="")
        
        # Act
        response = booking_api.create_booking(invalid_data)
        
        # Assert - API may accept or reject, but should not crash
        # Restful Booker actually accepts empty strings (it's a bug-practice API)
        assert response.status_code in [200, 400, 500], (
            f"Unexpected status {response.status_code}"
        )

    def test_create_booking_invalid_dates(self):
        """
        T011: Create booking - invalid dates (checkout < checkin).
        
        Verifies that booking with checkout before checkin is handled.
        """
        # Arrange
        booking_api = BookingApi()
        invalid_data = generate_booking_data(
            checkin="2024-12-25",
            checkout="2024-12-20"  # checkout BEFORE checkin
        )
        
        # Act
        response = booking_api.create_booking(invalid_data)
        
        # Assert - API should handle invalid dates
        # Note: Restful Booker may accept this (it's designed with bugs)
        assert response.status_code in [200, 400, 500], (
            f"Unexpected status {response.status_code}"
        )

    def test_create_booking_very_long_strings(self):
        """
        T012: Create booking - very long strings.
        
        Verifies that API handles extremely long field values.
        """
        # Arrange
        booking_api = BookingApi()
        long_string = "A" * 10000  # 10,000 characters
        long_data = generate_booking_data(
            firstname=long_string,
            lastname=long_string
        )
        
        # Act
        response = booking_api.create_booking(long_data)
        
        # Assert - should handle without crashing
        assert response.status_code in [200, 400, 413, 500], (
            f"Unexpected status {response.status_code}"
        )
        
        # If accepted, verify we can retrieve it
        if response.status_code == 200:
            booking_id = response.json()["bookingid"]
            get_response = booking_api.get_booking(booking_id)
            assert get_response.status_code == 200

    def test_create_booking_minimal_fields(self):
        """
        T013: Create booking - minimal required fields.
        
        Verifies that booking can be created with only required fields.
        """
        # Arrange - only required fields, no additionalneeds
        booking_api = BookingApi()
        minimal_data = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-05"
            }
        }
        
        # Act
        response = booking_api.create_booking(minimal_data)
        
        # Assert
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        assert "bookingid" in response_json
        assert response_json["booking"]["firstname"] == "John"

    def test_create_booking_duplicates_get_different_ids(self):
        """
        T014: Duplicates - identical data create different IDs.
        
        Verifies that two bookings with same data get unique IDs.
        """
        # Arrange
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        
        # Act - create two bookings with identical data
        response1 = booking_api.create_booking(booking_data)
        response2 = booking_api.create_booking(booking_data)
        
        # Assert - both should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # IDs should be different
        id1 = response1.json()["bookingid"]
        id2 = response2.json()["bookingid"]
        assert id1 != id2, (
            f"Duplicate bookings should have different IDs, got {id1} and {id2}"
        )

    def test_get_non_existent_booking(self):
        """
        T015: GET non-existent booking - 404.
        
        Verifies that GET for non-existent ID returns 404.
        """
        # Arrange
        booking_api = BookingApi()
        non_existent_id = 999999999  # Very large ID unlikely to exist
        
        # Act
        response = booking_api.get_booking(non_existent_id)
        
        # Assert
        assert response.status_code == 404, (
            f"Expected status 404, got {response.status_code}"
        )

