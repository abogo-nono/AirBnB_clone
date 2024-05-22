#!/usr/bin/python3
"""File storage
"""

import os
from models.base_model import BaseModel
import json


class FileStorage:
    """
    Class representing a file storage system for storing and managing objects in a JSON file.

    Attributes:
        CLASSES (dict): A dictionary mapping class names to their corresponding classes.
        __file_path (str): The path to the JSON file where objects are stored.
        __objects (dict): A dictionary to store objects with keys in the format 'ClassName.object_id'.

    Methods:
        all(self): Returns all objects stored in the FileStorage.
        
        new(self, obj): Adds a new object to the FileStorage __objects attribute.
        
        save(self): Saves the objects stored in the FileStorage to a JSON file.
        
        reload(self): Reloads the objects from a JSON file into the FileStorage.

    Raises:
        FileNotFoundError: If the file specified by __file_path is not found.
        JSONDecodeError: If the content of the file is not in a valid JSON format.

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

        This method iterates over the objects stored in the __objects attribute, serializes each object using its to_dict method, and then saves the serialized objects to a JSON file specified by the __file_path attribute.

        Args:
            self: The FileStorage instance.

        Returns:
            None
        """
        serialized_obj = {}

        for k, v in self.__objects.items():
            serialized_obj[k] = v.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_obj, file, indent=2)
            
    
    def reload(self):
        """
        Reload the objects from a JSON file into the FileStorage.

        This method reads the JSON file specified by the __file_path attribute, deserializes the content, and reconstructs the objects stored in the file. It iterates over the deserialized content, creates instances of the corresponding classes based on the '__class__' attribute, and stores these instances in the __objects attribute of the FileStorage instance.

        If the file is empty or not in a valid JSON format, it will raise a JSONDecodeError.

        Args:
            self: The FileStorage instance.

        Returns:
            None
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
                        print("Can't decode the content of the file. Seen like it's not a json format")
        except FileNotFoundError:
            print("file.json is not found!")