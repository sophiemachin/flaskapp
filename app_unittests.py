import unittest
from app import *

testSuite = unittest.TestSuite()


class RemovePunctuation(unittest.TestCase):
    def test_get_punc_to_remove(self):
        self.assertEqual(
            get_punc_to_remove(), """!"#$%&'()*+,./:;<=>?@[\]^_`{|}~""")

    def test_remove_punctuation_basic(self):
        s = 'test string!'
        punc_to_rem = '!()*'
        success = 'test string'
        self.assertEqual(remove_punctuation(s, punc_to_rem), success)

    def test_remove_punctuation_greek(self):
        s = 'test string with alpha α'
        punc_to_rem = '!()*'
        success = 'test string with alpha α'
        self.assertEqual(remove_punctuation(s, punc_to_rem), success)


class CountWords(unittest.TestCase):
    def test_count_words_basic(self):
        s = "count these words words words Words Words!"
        remove_capitals = True
        remove_punc = True
        self.assertEqual(
            count_words(s, remove_capitals, remove_punc),
            Counter({
                'words': 5,
                'count': 1,
                'these': 1,
            }))

    def test_count_words_caps(self):
        s = "count these words words words Words Words!"
        remove_capitals = False
        remove_punc = True
        self.assertEqual(
            count_words(s, remove_capitals, remove_punc),
            Counter({
                'words': 3,
                'count': 1,
                'these': 1,
                'Words': 2,
            }))

    def test_count_words_punc(self):
        s = "count these words words words Words Words!"
        remove_capitals = True
        remove_punc = False
        self.assertEqual(
            count_words(s, remove_capitals, remove_punc),
            Counter({
                'words': 4,
                'count': 1,
                'these': 1,
                'words!': 1,
            }))


if __name__ == "__main__":
    unittest.main()
