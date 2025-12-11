import concurrent.futures
from logic.auth_api import AuthApi
from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


class TestBookingConcurrency:
    """Concurrency tests for booking API (T021-T023)."""

    def test_concurrent_update_last_write_wins(self):
        """
        T021: Concurrent update - conflicting modifications.
        
        Verifies that simultaneous PUT requests to the same booking
        result in a consistent final state (last write wins).
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        initial_data = generate_booking_data()
        create_response = booking_api.create_booking(initial_data)
        booking_id = create_response.json()["bookingid"]
        
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Prepare two different updates
        update_data_1 = generate_booking_data(firstname="UpdateOne")
        update_data_2 = generate_booking_data(firstname="UpdateTwo")
        
        def do_update(data):
            """Perform update and return response."""
            return booking_api.update_booking(booking_id, data, token)
        
        # Act - send two updates concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(do_update, update_data_1)
            future2 = executor.submit(do_update, update_data_2)
            
            response1 = future1.result()
            response2 = future2.result()
        
        # Assert - both requests should succeed (or one may get conflict)
        assert response1.status_code in [200, 409], (
            f"Update 1 got unexpected status {response1.status_code}"
        )
        assert response2.status_code in [200, 409], (
            f"Update 2 got unexpected status {response2.status_code}"
        )
        
        # Final state should be consistent
        final_response = booking_api.get_booking(booking_id)
        assert final_response.status_code == 200
        
        final_firstname = final_response.json()["firstname"]
        assert final_firstname in ["UpdateOne", "UpdateTwo"], (
            f"Final state should be one of the updates, got {final_firstname}"
        )

    def test_concurrent_delete_and_read_race(self):
        """
        T022: Concurrent delete + read (race).
        
        Verifies that simultaneous DELETE and GET requests
        don't crash the system.
        """
        # Arrange - create booking and get token
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        def do_delete():
            return booking_api.delete_booking(booking_id, token)
        
        def do_get():
            return booking_api.get_booking(booking_id)
        
        # Act - send DELETE and GET concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            delete_future = executor.submit(do_delete)
            get_future = executor.submit(do_get)
            
            delete_response = delete_future.result()
            get_response = get_future.result()
        
        # Assert - DELETE should succeed
        assert delete_response.status_code in [200, 201], (
            f"DELETE got unexpected status {delete_response.status_code}"
        )
        
        # GET may return 200 (if executed before delete) or 404 (if after)
        assert get_response.status_code in [200, 404], (
            f"GET got unexpected status {get_response.status_code}"
        )
        
        # After everything, booking should be deleted
        verify_response = booking_api.get_booking(booking_id)
        assert verify_response.status_code == 404, (
            "Booking should be deleted after concurrent operations"
        )

    def test_teardown_cleanup_after_test(self):
        """
        T023: Teardown cleanup - delete resource after test.
        
        Verifies that test can create a booking and properly
        clean it up afterwards using authentication.
        """
        # Arrange
        booking_api = BookingApi()
        auth_api = AuthApi()
        
        # Create booking
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        assert create_response.status_code == 200
        booking_id = create_response.json()["bookingid"]
        
        # Get token for cleanup
        token_response = auth_api.create_token()
        token = token_response.json()["token"]
        
        # Act - perform some test operations
        get_response = booking_api.get_booking(booking_id)
        assert get_response.status_code == 200
        
        # Cleanup - delete the booking
        delete_response = booking_api.delete_booking(booking_id, token)
        
        # Assert - cleanup succeeded
        assert delete_response.status_code == 201, (
            f"Cleanup delete failed with status {delete_response.status_code}"
        )
        
        # Verify resource is removed
        verify_response = booking_api.get_booking(booking_id)
        assert verify_response.status_code == 404, (
            "Resource should be removed after cleanup"
        )

