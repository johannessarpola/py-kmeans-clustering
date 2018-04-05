from app.test.context import logger_factory
from app.test.context import path_to_resources
import os
import unittest

class LoggerFactoryTest(unittest.TestCase):
    test_log_file = 'test_log.log'
    test_log_folder = path_to_resources()

    def test_log_instance(self):
        p = os.path.join(self.test_log_folder, self.test_log_file)
        factory = logger_factory.LoggerFactory(self.test_log_folder,  self.test_log_file)
        logger = factory.instance("test_log")
        msg = "hello world"
        logger.debug(msg)
        self.assertTrue(os.path.exists(p))
        lines = open(p).read()
        self.assertEqual(1, len(open(p).readlines()))
        self.assertIn(msg, lines)
        factory.close()

    def test_log_multiple_instances(self):
        p = os.path.join(self.test_log_folder, self.test_log_file)
        factory = logger_factory.LoggerFactory(self.test_log_folder,  self.test_log_file)
        a = factory.instance("a")
        b = factory.instance("b")
        msg = "hello world"
        a.debug(msg)
        b.debug(msg)
        self.assertTrue(os.path.exists(p))
        ls = open(p).readlines()
        self.assertEqual(2, len(ls))
        for line in ls:
            self.assertIn(msg, line)
        factory.close()

    def tearDown(self):
        test_log_path = os.path.join(self.test_log_folder, self.test_log_file)
        os.remove(test_log_path)
