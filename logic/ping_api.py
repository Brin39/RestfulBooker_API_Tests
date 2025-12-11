from infra.base_api import BaseApi


class PingApi(BaseApi):
    """
    API client for health check endpoints.
    Used to verify that the API service is running and accessible.
    """

    def __init__(self):
        """
        Initialize PingApi with the base URL.
        Calls parent class constructor to set up the HTTP client.
        """
        super().__init__()

    def health_check(self):
        """
        Perform a health check on the API.
        
        Returns:
            Response object from the /ping endpoint
        """
        return self.send_request("GET", "/ping")

