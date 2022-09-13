import unittest
import models.models_mongo as model_db
from uuid import UUID, uuid4
from pydantic import Field


class TestApp(unittest.TestCase):
    def setUp(self):
        print("Setup code. Lets create a new db mock if there is no")
        if not hasattr(self, "db"):
            self.db = {}

    def tearDown(self):
        print("Clear after test")
        self.db.clear()

    def test_create_tag(self):
        new_tag = model_db.Tag(id="id_tag",
                               name="test_tag")
        self.assertEqual(isinstance(new_tag, "Tag"), True)


if __name__ == '__main__':
    unittest.main()