import json
from uuid import uuid4
from datetime import datetime
import os

class Person:
    def __init__(self) -> None:
        self.id = str(uuid4())
        self.created_at = str(datetime.now())
        self.updated_at = self.created_at
        

    def __str__(self) -> str:
        """
        Return a string representation of the Person object.

        This method returns a string that includes the creation and update timestamps of the Person object.
        The string is formatted as "Created at: {created_at} Updated at: {updated_at}".

        Returns:
            str: A string representation of the Person object.
        """
        return f"Created at: {self.created_at} Updated at: {self.updated_at}"


    def to_dict(self):
        """
        Return a dictionary containing the serialized representation of the Person object.

        This method creates a dictionary with a key-value pair where the key is generated using the 'new' method and the value is the serialized representation of the Person object obtained using the 'to_dict' method.
        The serialized representation includes all the properties of the Person object.
        The dictionary is then returned as the output of the method.

        Returns:
            dict: A dictionary containing the serialized representation of the Person object.
        """
        
        to_json = self.__dict__
        to_json['__class__'] = self.__class__.__name__
        return to_json
    
    def new(self):
        """
        Return a unique key for the Person object.

        This method generates a unique key for the Person object by combining the class name and the object's id.
        The key is returned as a string.

        Returns:
            str: A unique key for the Person object in the format "{class_name}.{id}".
        """
        
        key = f"{__class__.__name__}.{self.id}"
        return key

    
    def save(self):
        """
        Save the serialized representation of the Person object to a JSON file.

        This method first calls the 'reload' method to load the existing serialized objects from the JSON file into a dictionary.
        Then, it adds a new key-value pair to the dictionary, where the key is generated using the 'new' method and the value is the serialized representation of the Person object obtained using the 'to_dict' method.
        After that, it opens the JSON file in write mode and uses the 'json.dump' function to write the updated dictionary to the file in a human-readable format with an indentation level of 2.

        Parameters:
            None

        Returns:
            None
        """
        
        serialized_obj = self.reload()
        
        serialized_obj[self.new()] = self.to_dict()
        
        with open('file.json', 'w') as file:
            json.dump(serialized_obj, file, indent=2)
    
    
    def reload(self):
        """
        Load the serialized objects from a JSON file and return them as a dictionary.

        This method opens the specified JSON file in read mode and checks if the file is not empty.
        If the file is not empty, it uses the 'json.load' function to load the content of the file into a dictionary.
        Then, it iterates over the key-value pairs in the dictionary and adds them to a new dictionary called 'serialized_obj'.
        Finally, it returns the 'serialized_obj' dictionary as the output of the method.

        Returns:
            dict: A dictionary containing the serialized objects loaded from the JSON file.

        Raises:
            JSONDecodeError: If the content of the file cannot be decoded as JSON.

        Example:
            >>> person = Person()
            >>> serialized_objects = person.reload()
            >>> print(serialized_objects)
            {'Person.12345': {'id': '12345', 'created_at': '2022-01-01 12:00:00', 'updated_at': '2022-01-01 12:00:00'}}
        """
        
        serialized_obj = {}
        with open('file.json', 'r') as file:
            if os.path.getsize('./file.json') > 0:
                try:
                    content = json.load(file)
                    for k, v in content.items():
                        serialized_obj[k] = v
                        # print(f"key={k} value={v}",  end='\n')
                except json.decoder.JSONDecodeError:
                    print("Can't decode the content of the file. Seen like it's not a json format")
        return serialized_obj
        
    
        

person1 = Person()
print(person1)
person1.save()
