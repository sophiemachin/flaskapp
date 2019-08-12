import unittest
from app import *

testSuite = unittest.TestSuite()


class MyTest(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(hello_world(), 'Hello, World!')


if __name__ == "__main__":
    unittest.main()
