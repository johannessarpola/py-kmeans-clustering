import unittest
from app.src import models


class ModelTest(unittest.TestCase):
    def test_vectorization(self):
        doc = models.Document("a", 1, 1, "str", ["abc:1", "cba:2", "bac:3"])
        d = doc.vector_dict()
        self.assertEqual(1, d["abc"])
        self.assertEqual(2, d["cba"])
        self.assertEqual(3, d["bac"])

    def test_vectorization_with_normalized(self):
        doc = models.Document("a", 10, 1, "str", ["abc:2.0", "ccc:1.25", "cba:1.5", "bac:1"])
        d = doc.vector_dict()
        self.assertEqual(10, d["abc"])
        self.assertEqual(5.5, d["cba"])
        self.assertEqual(3.25, d["ccc"])
        self.assertEqual(1, d["bac"])

    def test_vectorization_with_non_normalized(self):
        doc = models.Document("a", 10, 1, "str", ["abc:2.0", "cba:1.5", "bac:1"])
        d = doc.vector_dict(normalized=False)
        self.assertEqual(2, d["abc"])
        self.assertEqual(1.5, d["cba"])
        self.assertEqual(1, d["bac"])


if __name__ == '__main__':
    unittest.main()