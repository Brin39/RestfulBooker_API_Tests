

import httpx
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseApi:
    """
    Base API client for making HTTP requests to the Restful Booker API.
    This class handles the core HTTP communication.
    """

    def __init__(self, base_url="https://restful-booker.herokuapp.com"):
        """
        Initialize the API client with a base URL.

        Args:
            base_url: The base URL of the API (default: Restful Booker URL)
        """
        self.base_url = base_url
        logger.info(f"Initialized API client with base URL: {base_url}")

    def send_request(self, method, endpoint, payload=None, headers=None, cookies=None):
        """
        Send an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (e.g., /booking)
            payload: Request body data (dictionary)
            headers: HTTP headers (dictionary)
            cookies: Request cookies (dictionary)

        Returns:
            Response object from the httpx library
        """
        # Construct the full URL
        url = f"{self.base_url}{endpoint}"

        # Set default headers if none provided
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

        # Log request details
        logger.info(f"Sending {method} request to: {url}")
        if payload:
            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
        if headers:
            logger.debug(f"Request headers: {headers}")

        # Prepare request kwargs
        request_kwargs = {
            "headers": headers,
            "cookies": cookies
        }

        # Add JSON payload for appropriate methods
        if payload and method.upper() in ["POST", "PUT", "PATCH"]:
            request_kwargs["json"] = payload

        try:
            # Create a client and send the request
            with httpx.Client() as client:
                response = client.request(method, url, **request_kwargs)

            # Log response details
            logger.info(f"Response status code: {response.status_code}")
            try:
                logger.debug(f"Response body: {json.dumps(response.json(), indent=2)}")
            except json.JSONDecodeError:
                logger.debug(f"Response body: {response.text}")

            return response

        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise