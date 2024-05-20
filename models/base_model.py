from datetime import datetime
from uuid import uuid4
# from models import storage
import models

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
            models.storage.new(self)
        
    
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()
        
        
    def to_dict(self) -> dict:
        to_json = self.__dict__
        to_json['__class__'] = self.__class__.__name__
        to_json['created_at'] = to_json['created_at'].isoformat()
        to_json['updated_at'] = to_json['updated_at'].isoformat()

        return to_json


