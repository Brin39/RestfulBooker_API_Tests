from infra.base_api import BaseApi


class BookingApi(BaseApi):
    """
    API client for booking endpoints.
    Handles CRUD operations for hotel bookings.
    """

    def __init__(self):
        """
        Initialize BookingApi with the base URL.
        """
        super().__init__()

    def _get_auth_headers(self, token):
        """
        Get headers with authentication token.
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary with headers including auth cookie
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }

    def get_all_bookings(self):
        """
        Get list of all booking IDs.
        
        Returns:
            Response with array of booking IDs
        """
        return self.send_request("GET", "/booking")

    def get_booking(self, booking_id):
        """
        Get a specific booking by ID.
        
        Args:
            booking_id: The ID of the booking to retrieve
            
        Returns:
            Response with booking details
        """
        return self.send_request("GET", f"/booking/{booking_id}")

    def create_booking(self, booking_data):
        """
        Create a new booking.
        
        Args:
            booking_data: Dictionary with booking details
            
        Returns:
            Response with created booking and bookingid
        """
        return self.send_request("POST", "/booking", payload=booking_data)

    def update_booking(self, booking_id, booking_data, token):
        """
        Full update of a booking (PUT).
        Requires authentication token.
        
        Args:
            booking_id: The ID of the booking to update
            booking_data: Complete booking data
            token: Authentication token
            
        Returns:
            Response with updated booking
        """
        return self.send_request(
            "PUT",
            f"/booking/{booking_id}",
            payload=booking_data,
            headers=self._get_auth_headers(token)
        )

    def partial_update_booking(self, booking_id, booking_data, token):
        """
        Partial update of a booking (PATCH).
        Requires authentication token.
        
        Args:
            booking_id: The ID of the booking to update
            booking_data: Partial booking data (only fields to update)
            token: Authentication token
            
        Returns:
            Response with updated booking
        """
        return self.send_request(
            "PATCH",
            f"/booking/{booking_id}",
            payload=booking_data,
            headers=self._get_auth_headers(token)
        )

    def delete_booking(self, booking_id, token):
        """
        Delete a booking.
        Requires authentication token.
        
        Args:
            booking_id: The ID of the booking to delete
            token: Authentication token
            
        Returns:
            Response (typically 201 on success)
        """
        return self.send_request(
            "DELETE",
            f"/booking/{booking_id}",
            headers=self._get_auth_headers(token)
        )

