import json


class BaseModel:
    """Base class for all models in the application."""

    def to_dict(self):
        """Convert model to dictionary representation."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def to_json(self):
        """Convert model to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data_dict):
        """Create model instance from dictionary."""
        instance = cls()
        for key, value in data_dict.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance

    @classmethod
    def from_json(cls, json_string):
        """Create model instance from JSON string."""
        data_dict = json.loads(json_string)
        return cls.from_dict(data_dict)