
import unittest
import uuid
import datetime
from models.base_model import BaseModel
from models import storage


class TestBase(unittest.TestCase):

    def test_initialization_no_kwargs(self):
        bm = BaseModel()
        self.assertIsInstance(uuid.UUID(bm.id), uuid.UUID)
        self.assertIsInstance(bm.created_at, datetime.datetime)
        self.assertIsInstance(bm.updated_at, datetime.datetime)

    def test_initialise_with_kwargs(self):
        kwargs = {
            'id': str(uuid.uuid4()),
            'created_at': '2022-02-15T12:34:56.789012',
            'updated_at': '2022-02-15T12:34:56.789012',
        }
        bm = BaseModel(**kwargs)
        self.assertIsInstance(uuid.UUID(bm.id), uuid.UUID)
        self.assertEqual(bm.created_at.isoformat(), kwargs['created_at'])
        self.assertEqual(bm.updated_at.isoformat(), kwargs['updated_at'])

    def test___str__(self):
        kwargs = {
            'id': str(uuid.uuid4()),
            'created_at': '2022-02-15T12:34:56.789012',
            'updated_at': '2022-02-15T12:34:56.789012',
        }
        bm = BaseModel(**kwargs)
        self.assertEqual(str(bm), "[BaseModel] ({}) {}".format
                         (kwargs['id'], bm.__dict__))

    def test_save_method(self):
        bm = BaseModel()
        original_updated_at = bm.updated_at
        bm.save()
        self.assertNotEqual(bm.updated_at, original_updated_at)

    def test_to_dict_method(self):
        bm = BaseModel()
        base_dict = bm.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertIn('__class__', base_dict)
        self.assertIn('id', base_dict)
        self.assertIn('created_at', base_dict)
        self.assertIn('updated_at', base_dict)

    def test_storage_interaction(self):
        bm = BaseModel()
        bm.save()
        self.assertIn(f"{bm.__class__.__name__}.{bm.id}", storage.all())

    def test_edge_cases(self):
        pass

if __name__ == "__main__":
    unittest.main()
