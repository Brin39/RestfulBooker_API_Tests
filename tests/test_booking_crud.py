from logic.auth_api import AuthApi
from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data, generate_partial_booking_data


class TestBookingCRUD:
    """Tests for booking CRUD operations (T001-T005)."""

    def test_create_booking_success(self):
        """
        T001: Create booking - successful creation.
        
        Verifies that POST /booking creates a new booking
        and returns bookingid with booking details.
        """
        # Arrange
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        
        # Act
        response = booking_api.create_booking(booking_data)
        
        # Assert
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        assert "bookingid" in response_json, (
            "Response should contain bookingid"
        )
        assert response_json["bookingid"], (
            "bookingid should not be empty"
        )
        assert "booking" in response_json, (
            "Response should contain booking object"
        )
        
        # Verify booking fields match sent data
        booking = response_json["booking"]
        assert booking["firstname"] == booking_data["firstname"]
        assert booking["lastname"] == booking_data["lastname"]
        assert booking["totalprice"] == booking_data["totalprice"]

    def test_get_booking_by_id(self):
        """
        T002: Get booking by id - return created booking.
        
        Verifies that GET /booking/{id} returns the correct booking.
        """
        # Arrange - create a booking first
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Act
        response = booking_api.get_booking(booking_id)
        
        # Assert
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        assert response_json["firstname"] == booking_data["firstname"]
        assert response_json["lastname"] == booking_data["lastname"]
        assert response_json["totalprice"] == booking_data["totalprice"]
        assert response_json["depositpaid"] == booking_data["depositpaid"]

    def test_update_booking_full(self):
        """
        T003: Update booking (PUT) - full update.
        
        Verifies that PUT /booking/{id} updates all booking fields.
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        # Create initial booking
        initial_data = generate_booking_data()
        create_response = booking_api.create_booking(initial_data)
        booking_id = create_response.json()["bookingid"]
        
        # Get auth token
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Prepare updated data (all new values)
        updated_data = generate_booking_data()
        
        # Act
        response = booking_api.update_booking(booking_id, updated_data, token)
        
        # Assert
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        assert response_json["firstname"] == updated_data["firstname"]
        assert response_json["lastname"] == updated_data["lastname"]
        assert response_json["totalprice"] == updated_data["totalprice"]
        
        # Verify with GET request
        get_response = booking_api.get_booking(booking_id)
        get_json = get_response.json()
        assert get_json["firstname"] == updated_data["firstname"]

    def test_partial_update_booking(self):
        """
        T004: Partial update (PATCH) - change single field.
        
        Verifies that PATCH /booking/{id} updates only specified field.
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        # Create initial booking
        initial_data = generate_booking_data()
        create_response = booking_api.create_booking(initial_data)
        booking_id = create_response.json()["bookingid"]
        
        # Get auth token
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Prepare partial update (only firstname)
        new_firstname = "UpdatedName"
        patch_data = generate_partial_booking_data("firstname", new_firstname)
        
        # Act
        response = booking_api.partial_update_booking(booking_id, patch_data, token)
        
        # Assert
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}"
        )
        
        response_json = response.json()
        # Changed field should be updated
        assert response_json["firstname"] == new_firstname
        # Other fields should remain unchanged
        assert response_json["lastname"] == initial_data["lastname"]
        assert response_json["totalprice"] == initial_data["totalprice"]

    def test_delete_booking_success(self):
        """
        T005: Delete booking - successful deletion.
        
        Verifies that DELETE /booking/{id} removes the booking.
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        # Create booking to delete
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Get auth token
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Act
        response = booking_api.delete_booking(booking_id, token)
        
        # Assert - DELETE returns 201 in this API
        assert response.status_code == 201, (
            f"Expected status 201, got {response.status_code}"
        )
        
        # Verify booking is deleted (GET should return 404)
        get_response = booking_api.get_booking(booking_id)
        assert get_response.status_code == 404, (
            f"Expected status 404 for deleted booking, got {get_response.status_code}"
        )

