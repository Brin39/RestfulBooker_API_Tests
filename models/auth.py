from .base_model import BaseModel


class AuthCredentials(BaseModel):
    """Model representing authentication credentials."""

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password


class AuthToken(BaseModel):
    """Model representing an authentication token."""

    def __init__(self, token=None):
        self.token = token