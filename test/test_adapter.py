import unittest
import json
from context import adapter,relative_resource

class ModelTest(unittest.TestCase):
    def test_document_adapter(self):
        path = relative_resource('docs.json')
        file = open(path)
        documents_json = json.load(file)
        file.close()
        models = adapter.multiple_documents_from_json(documents_json)
        self.assertEqual(2, len(models))
        ids = map(lambda d: d.id, models)
        self.assertIn('a7e5dd40dc2ace0b38187c2ef6909ec2f4a59e3b213a1f0e877aabf25cbb618c', ids)
        self.assertIn('77c7f61b07ecbde18864761f8e473051f0ab80780e96d2728c7c4b8dc029a258', ids)

    def test_document_hash_adapter(self):
        path = relative_resource('hashes.json')
        file = open(path, "r")
        documents_json = json.load(file)
        file.close()
        models = adapter.multiple_document_hashes_from_json(documents_json)
        self.assertEqual(2, len(models))
        ids = list(map(lambda d: d.id, models))
        attributes = list(map(lambda d: d.attributes, models))
        self.assertIn('a7e5dd40dc2ace0b38187c2ef6909ec2f4a59e3b213a1f0e877aabf25cbb618c', ids)
        self.assertIn('77c7f61b07ecbde18864761f8e473051f0ab80780e96d2728c7c4b8dc029a258', ids)
        self.assertEqual(4, len(attributes[0]))
        self.assertEqual(2, len(attributes))

    def test_cluster_dict_to_array_json(self):
        d = {}
        d["a"] = ["a", "a", "a"]
        d["b"] = ["b", "b", "b"]
        re = adapter.cluster_dict_to_obj_array(d)
        self.assertEqual(2, len(re))
        self.assertEqual("a", re[0].id)
        self.assertEqual("b", re[1].id)

        self.assertEqual(3, len(re[1].clusters))
        self.assertEqual(3, len(re[1].clusters))



if __name__ == '__main__':
    unittest.main()
