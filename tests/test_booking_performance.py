import time
import concurrent.futures
from logic.booking_api import BookingApi
from utils.test_data import generate_booking_data


class TestBookingPerformance:
    """Performance tests for booking API (T019-T020)."""

    def test_response_time_within_sla(self):
        """
        T019: SLA - response time for critical operation.
        
        Verifies that POST /booking responds within acceptable time limit.
        SLA threshold: 5000ms (5 seconds) - adjusted for parallel execution and demo API
        """
        # Arrange
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        sla_threshold_ms = 5000  # 5 seconds (accounts for parallel load and Heroku)
        
        # Act - measure response time
        start_time = time.time()
        response = booking_api.create_booking(booking_data)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Assert
        assert response.status_code == 200, (
            f"Request failed with status {response.status_code}"
        )
        assert response_time_ms < sla_threshold_ms, (
            f"Response time {response_time_ms:.0f}ms exceeded SLA threshold {sla_threshold_ms}ms"
        )

    def test_get_booking_response_time(self):
        """
        T019 (extended): Verify GET response time is within SLA.
        """
        # Arrange - create a booking first
        booking_api = BookingApi()
        booking_data = generate_booking_data()
        create_response = booking_api.create_booking(booking_data)
        booking_id = create_response.json()["bookingid"]
        sla_threshold_ms = 5000  # 5 seconds
        
        # Act - measure GET response time
        start_time = time.time()
        response = booking_api.get_booking(booking_id)
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        
        # Assert
        assert response.status_code == 200
        assert response_time_ms < sla_threshold_ms, (
            f"GET response time {response_time_ms:.0f}ms exceeded SLA {sla_threshold_ms}ms"
        )

    def test_parallel_booking_creation(self):
        """
        T020: Parallel creation of N bookings.
        
        Verifies that multiple concurrent booking requests
        all succeed and return unique IDs.
        """
        # Arrange
        booking_api = BookingApi()
        num_parallel_requests = 5  # Number of parallel bookings
        
        def create_single_booking():
            """Helper function to create one booking."""
            data = generate_booking_data()
            response = booking_api.create_booking(data)
            return response
        
        # Act - send N requests in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_parallel_requests) as executor:
            futures = [
                executor.submit(create_single_booking)
                for _ in range(num_parallel_requests)
            ]
            responses = [
                future.result()
                for future in concurrent.futures.as_completed(futures)
            ]
        
        # Assert - all requests should succeed
        booking_ids = []
        for i, response in enumerate(responses):
            assert response.status_code == 200, (
                f"Parallel request {i+1} failed with status {response.status_code}"
            )
            booking_id = response.json()["bookingid"]
            booking_ids.append(booking_id)
        
        # All IDs should be unique
        assert len(booking_ids) == len(set(booking_ids)), (
            f"Expected {num_parallel_requests} unique IDs, got duplicates: {booking_ids}"
        )

    def test_parallel_requests_no_errors(self):
        """
        T020 (extended): Verify no errors or timeouts during parallel load.
        """
        # Arrange
        booking_api = BookingApi()
        num_requests = 10
        results = {"success": 0, "failed": 0, "errors": []}
        
        def make_request(request_num):
            """Make a single request and track result."""
            try:
                data = generate_booking_data()
                response = booking_api.create_booking(data)
                if response.status_code == 200:
                    return {"status": "success", "id": response.json()["bookingid"]}
                else:
                    return {"status": "failed", "code": response.status_code}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        
        # Act - parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result["status"] == "success":
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(result)
        
        # Assert - all should succeed
        assert results["success"] == num_requests, (
            f"Expected {num_requests} successes, got {results['success']}. "
            f"Errors: {results['errors']}"
        )

