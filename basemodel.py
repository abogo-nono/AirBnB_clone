import os
from datetime import datetime
from uuid import uuid4
import json


class BaseModel:
    def __init__(self, **kwargs) -> None:
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                if k in ['created_at', 'updated_at']:
                    v = datetime.fromisoformat(v)
                setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        
    
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


    def save(self):
        self.updated_at = datetime.now()
        
        
    def to_dict(self) -> dict:
        to_json = self.__dict__
        to_json['__class__'] = self.__class__.__name__
        to_json['created_at'] = to_json['created_at'].isoformat()
        to_json['updated_at'] = to_json['updated_at'].isoformat()

        return to_json

    
model = BaseModel()


class FileStorage:
    CLASSES = {'BaseModel': BaseModel}
    __file_path = "file.json"
    __objects = {}
    
    def all(self):
        return self.__objects
    
    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

        
    def save(self):
        serialized_obj = {}

        for k, v in self.__objects.items():
            serialized_obj[k] = v.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_obj, file, indent=2)
            
    
    def reload(self):
        with open(self.__file_path, 'r') as file:
            content = json.load(file)
        
        for k, v in content.items():
            class_name = v['__class__']
            
            if class_name in self.CLASSES:
                instance = self.CLASSES[class_name](**v)
                self.__objects[k] = instance
            
            

storage = FileStorage()
storage.new(model)
all_obj = storage.all()
storage.reload()
storage.save()