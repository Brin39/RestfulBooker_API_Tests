from infra.base_api import BaseApi


class AuthApi(BaseApi):
    """
    API client for authentication endpoints.
    Handles token creation for accessing protected resources.
    """

    # Default credentials for the Restful Booker API
    DEFAULT_USERNAME = "admin"
    DEFAULT_PASSWORD = "password123"

    def __init__(self):
        """
        Initialize AuthApi with the base URL.
        Calls parent class constructor to set up the HTTP client.
        """
        super().__init__()

    def create_token(self, username=None, password=None):
        """
        Create an authentication token.
        
        Args:
            username: Username for authentication (default: admin)
            password: Password for authentication (default: password123)
            
        Returns:
            Response object from the /auth endpoint
        """
        # Use default credentials if not provided
        payload = {
            "username": username if username is not None else self.DEFAULT_USERNAME,
            "password": password if password is not None else self.DEFAULT_PASSWORD
        }
        
        return self.send_request("POST", "/auth", payload=payload)

