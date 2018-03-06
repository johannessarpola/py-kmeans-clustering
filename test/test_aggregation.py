import unittest
import json
from context import aggregation,relative_resource

class Object(object):
    id = ''
    content = ''

    def __init__(self, id, content):
        self.id = id
        self.content = content


class AggregationTest(unittest.TestCase):
    def test_group_by_field(self):
        albums = json.load(open(relative_resource('albums.json')))
        result = aggregation.group_by_field(albums, 'userId')
        self.assertEqual(10, len(result))
        for i in range(1, 11):
            self.assertIn(str(i), result)

    def test_group_by_attribute(self):
        objs = [Object(1,"abc"), Object(2,"abc"), Object(3,"cba")]
        result = aggregation.group_by_attribute(objs, 'content')
        self.assertEqual(2, len(result))
        self.assertEqual(2, len(result["abc"]))
        self.assertEqual(1, len(result["cba"]))

if __name__ == '__main__':
    unittest.main()
