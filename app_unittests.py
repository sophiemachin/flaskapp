import unittest
from app import *

testSuite = unittest.TestSuite()


class MyTest(unittest.TestCase):
    def test_get_punc_to_remove(self):
        self.assertEqual(
            get_punc_to_remove(), """!"#$%&'()*+,./:;<=>?@[\]^_`{|}~""")


if __name__ == "__main__":
    unittest.main()
