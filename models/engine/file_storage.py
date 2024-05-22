#!/usr/bin/python3
"""File storage
"""

import os
from models.base_model import BaseModel
import json


class FileStorage:
    """
    Class representing a file storage system for storing and
    managing objects in a JSON file.

    """

    CLASSES = {'BaseModel': BaseModel}
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        """
        Add a new object to the FileStorage __objects attribute.

        Args:
            obj: BaseModel object to be added to the storage.

        Returns:
            None
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Save the objects stored in the FileStorage to a JSON file.
        """
        serialized_obj = {}

        for k, v in self.__objects.items():
            serialized_obj[k] = v.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_obj, file, indent=2)

    def reload(self):
        """
        Reload the objects from a JSON file into the FileStorage.
        """
        try:
            with open(self.__file_path, 'r') as file:
                if os.path.getsize(self.__file_path) > 0:
                    try:
                        content = json.load(file)

                        for k, v in content.items():
                            class_name = v['__class__']

                            if class_name in self.CLASSES:
                                instance = self.CLASSES[class_name](**v)
                                self.__objects[k] = instance
                    except json.decoder.JSONDecodeError:
                        print("Seen like it's not a json format")
        except FileNotFoundError:
            print("file.json is not found!")
