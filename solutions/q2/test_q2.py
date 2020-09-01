import unittest
from util import *
from encoder_lzss import *
from decoder_lzss import *


class TestCodec(unittest.TestCase):
    def check(self, string, window_range=31, lookahead_range=31):
        original_size = len(string) * 7
        for window in range(31):
            for lookahead in range(31):
                bits = compress_lzss(string, window, lookahead)
                decomp = decompress_lzss(bits)
                print(f'\rW: {window} L: {lookahead} Size(bits): {original_size} -> {bits.length()} -> {len(decomp) * 7}', end='')
                self.assertEqual(string, decomp)
        print()

    def test_codec(self):
        tests = [
            'single.txt',
            'double.txt',
            'lorem_ipsum.txt'
        ]
        for test in tests:
            test_string = read_file('./29352258/q2/tests/' + test)
            print('Test file:', test)
            self.check(test_string)
        empty_string = ''
        self.assertRaises(TypeError, compress_lzss, empty_string, 1, 1)


if __name__ == "__main__":
    unittest.main(failfast=False)
