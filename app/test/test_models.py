import unittest
from app.test.context import models


class ModelTest(unittest.TestCase):
    def test_vectorization(self):
        doc = models.Document("a", 1, 1, "str", ["abc:1", "cba:2", "bac:3"])
        d = doc.vector_dict()
        self.assertEqual(1, d["abc"])
        self.assertEqual(2, d["cba"])
        self.assertEqual(3, d["bac"])

if __name__ == '__main__':
    unittest.main()