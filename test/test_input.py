import unittest
from context import input_output,path_to_resources

class ModelTest(unittest.TestCase):
    def test_get_jsons_from_folder(self):
        files = input_output.get_jsons_from_folder(path_to_resources())
        names = input_output.get_filepaths_in_folder(path_to_resources())
        self.assertEqual(len(files), len(names))
        self.assertGreater(len(names), 1)
        self.assertGreater(len(files), 1)

if __name__ == '__main__':
    unittest.main()