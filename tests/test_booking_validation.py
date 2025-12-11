from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


class TestBookingValidation:
    """Tests for response schema and headers (T016-T017)."""

    def test_booking_response_matches_schema(self):
        """
        T016: JSON schema - response matches schema.
        
        Verifies that GET /booking/{id} response contains
        all required fields with correct types.
        """
        # Arrange - create a booking
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        # Act
        response = booking_api.get_booking(booking_id)
        response_json = response.json()
        
        # Assert - verify schema structure
        assert response.status_code == 200
        
        # Required fields must exist
        required_fields = ["firstname", "lastname", "totalprice",
                          "depositpaid", "bookingdates"]
        for field in required_fields:
            assert field in response_json, (
                f"Required field '{field}' missing from response"
            )
        
        # Verify field types
        assert isinstance(response_json["firstname"], str), (
            "firstname should be a string"
        )
        assert isinstance(response_json["lastname"], str), (
            "lastname should be a string"
        )
        assert isinstance(response_json["totalprice"], (int, float)), (
            "totalprice should be a number"
        )
        assert isinstance(response_json["depositpaid"], bool), (
            "depositpaid should be a boolean"
        )
        assert isinstance(response_json["bookingdates"], dict), (
            "bookingdates should be an object"
        )
        
        # Verify nested bookingdates structure
        bookingdates = response_json["bookingdates"]
        assert "checkin" in bookingdates, "checkin missing from bookingdates"
        assert "checkout" in bookingdates, "checkout missing from bookingdates"
        assert isinstance(bookingdates["checkin"], str), (
            "checkin should be a string"
        )
        assert isinstance(bookingdates["checkout"], str), (
            "checkout should be a string"
        )

    def test_response_headers_content_type(self):
        """
        T017: Response headers - Content-Type and others.
        
        Verifies that API responses contain correct headers.
        """
        # Arrange
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        
        # Act - test POST response headers
        post_response = booking_api.create_booking(booking_data)
        booking_id = post_response.json()["bookingid"]
        
        # Act - test GET response headers
        get_response = booking_api.get_booking(booking_id)
        
        # Assert - POST headers
        assert "content-type" in post_response.headers, (
            "Content-Type header missing from POST response"
        )
        post_content_type = post_response.headers["content-type"].lower()
        assert "application/json" in post_content_type, (
            f"Expected application/json, got {post_content_type}"
        )
        
        # Assert - GET headers
        assert "content-type" in get_response.headers, (
            "Content-Type header missing from GET response"
        )
        get_content_type = get_response.headers["content-type"].lower()
        assert "application/json" in get_content_type, (
            f"Expected application/json, got {get_content_type}"
        )

    def test_create_booking_response_schema(self):
        """
        T016 (extended): Verify POST /booking response schema.
        
        POST response should contain both bookingid and booking object.
        """
        # Arrange
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        
        # Act
        response = booking_api.create_booking(booking_data)
        response_json = response.json()
        
        # Assert - top level structure
        assert response.status_code == 200
        assert "bookingid" in response_json, "bookingid missing from response"
        assert "booking" in response_json, "booking object missing from response"
        
        # Assert - bookingid type
        assert isinstance(response_json["bookingid"], int), (
            "bookingid should be an integer"
        )
        
        # Assert - booking object structure
        booking = response_json["booking"]
        required_fields = ["firstname", "lastname", "totalprice",
                          "depositpaid", "bookingdates"]
        for field in required_fields:
            assert field in booking, (
                f"Required field '{field}' missing from booking object"
            )

