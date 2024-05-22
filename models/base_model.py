#!/usr/bin/python3
"""Base model
"""

from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    """
    BaseModel class represents a base model for other classes to inherit from.
    It provides methods for initialization, string representation,
    saving instances, and converting instances
    to dictionaries for serialization.

    Attributes:
        id (str): A unique identifier generated using uuid4.
        created_at (datetime): The date and time when the instance was created.
        updated_at (datetime): The date and time when
        the instance was last updated.

    Methods:
        __init__(self, **kwargs): Initialize a new instance of
            the BaseModel class.
        __str__(self): Return a string representation of the BaseModel instance
        save(self): Save the current instance by updating the 'updated_at'
            attribute and persisting changes.
        to_dict(self): Return a dictionary representation of
            the BaseModel instance for serialization.

    Returns:
        None
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize a new instance of the BaseModel class.

        Parameters:
            **kwargs (dict): Arbitrary keyword arguments to initialize
                the instance attributes.

        Attributes:
            id (str): A unique identifier generated using uuid4.
            created_at (datetime): The date and time when
                the instance was created.
            updated_at (datetime): The date and time when
                the instance was last updated.

        Returns:
            None
        """
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                if k in ['created_at', 'updated_at']:
                    v = datetime.strptime(v, self.TIME_FORMAT)
                setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self) -> str:
        """
        Return a string representation of the BaseModel instance.

        Returns:
            str: A string containing the class name, id, and dictionary
                of instance attributes.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Save the current instance by updating the 'updated_at' attribute
            with the current date and time, then call the 'save' method
            of the storage module to persist the changes.

        Parameters:
            None

        Returns:
            None
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the BaseModel instance,
            including all instance attributes and necessary metadata
            for serialization.

        Parameters:
            None

        Returns:
            dict: A dictionary containing the instance attributes
                along with '__class__', 'created_at',
                and 'updated_at' metadata in ISO format.
        """
        to_json = self.__dict__.copy()
        to_json['__class__'] = self.__class__.__name__

        for k, v in to_json.items():
            if isinstance(v, datetime):
                to_json[k] = v.isoformat()

        return to_json
