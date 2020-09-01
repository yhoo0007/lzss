from bitarray import bitarray, util
from util import *


def z_algo(string, current_index, window, lookahead):
    '''
    Performs Gusfield's Z-algorithm on the given string and returns the resulting Z-array.
        string:         String of characters as input to the Z-algorithm.
        current_index:  Index in the string where the prefix begins.
        window:         Size of the lookbehind window.
        lookahead:      Size of the lookahead window.
    '''
    start = max(0, current_index - window)
    end = min(len(string), current_index + lookahead)
    z = [0] * (end - start)

    # preprocess prefix
    l, r = 0, 0
    for i in range(current_index + 1, end):
        z_index = i - start
        if i > r:  # case 1: i not in zbox
            j = i
            while j < end and string[j] == string[j - i + current_index]:
                z[z_index] += 1
                j += 1
            if z[z_index] > 0:  # form zbox
                l, r = i, j - 1
        else:
            k = i - l + current_index - start
            remaining = r - i + 1
            if z[k] < remaining:  # case 2a
                z[z_index] = z[k]
            elif z[k] > remaining:  # case 2b
                z[z_index] = remaining
            else:  # case 2c
                z[z_index] = z[k]
                matches = 0
                j = r + 1
                k = z[z_index]
                while j < end and string[j] == string[k]:
                    z[z_index] += 1
                    matches += 1
                    j += 1
                    k += 1
                if matches > 0:  # form zbox
                    l, r = i, j - 1
    
    # process suffix
    l, r = -1, -1
    for i in range(start, current_index):
        z_index = i - start
        if i > r:  # case 1: i not in zbox
            j = i
            while j - i + current_index < end and string[j] == string[j - i + current_index]:
                z[z_index] += 1
                j += 1
            if z[z_index] > 0:  # form zbox
                l, r = i, j - 1
        else:
            k = i - l + current_index - start
            remaining = r - i + 1
            if z[k] < remaining:  # case 2a
                z[z_index] = z[k]
            elif z[k] > remaining:  # case 2b
                z[z_index] = remaining
            else:  # case 2c
                z[z_index] = z[k]
                matches = 0
                j = r + 1
                k += remaining
                while k + start < end and string[j] == string[k + start]:
                    z[z_index] += 1
                    matches += 1
                    j += 1
                    k += 1
                if matches > 0:  # form zbox
                    l, r = i, j - 1
    return z


def find_ls(z_array, end_index):
    '''
    Given a z array and an end index, find the right-most maximum value in the z array within the
    given end index.
        z_array:    Arbitrary array containing integers.
        end_index:  The right-most index in which the function will search to (non-inclusive).
    '''
    ls_len = 0
    ls_index = 0
    for i in range(end_index):
        n = z_array[i]
        if n >= ls_len:  # le such that we find the right most index
            ls_len = n
            ls_index = i
    return ls_len, ls_index


def get_freqs(string):
    '''
    Returns a frequency table of occurances of all characters in the given string.
        string: String to calculate occurrance frequency of.
    '''
    freqs = [[chr(i), 0] for i in range(128)]
    for c in string:
        freqs[ord(c)][1] += 1
    freqs = list(filter(lambda occ: occ[1] > 0, freqs))
    return freqs


def compress_lzss(text, window, lookahead):
    '''
    Returns a bitarray representing the LZSS compressed text in header and data parts.
        text:       String of ASCII characters to compress.
        window:     Size of the lookbehind window.
        lookahead:  Size of the lookahead window.
    '''
    if len(text) == 0:
        raise TypeError('Cannot compress empty text!')

    freqs = get_freqs(text)
    h_code = huffman_code(freqs)
    bits = elias_code(len(freqs))
    for i, code in enumerate(h_code):
        if code is not None:
            bits += util.int2ba(i, 7)  # ASCII of char padded to 7 bits
            bits += elias_code(code.length())
            bits += code

    # encode data
    n = len(text)
    n_format = 0
    data_bits = bitarray()
    i = 0
    while i < n:
        # find the longest substring in [i-window:i] which matches a prefix of [i:i+lookahead]
        z_array = z_algo(text, i, window, lookahead)
        ls_len, ls_index = find_ls(z_array, min(i, window))

        # calculate the encoding values
        if ls_len >= 3:  # format 0 <0-bit, offset, length>
            enc = bitarray('0') + \
                  elias_code(i - (max(0, i - window) + ls_index)) + \
                  elias_code(ls_len)
            i += ls_len
        else:  # format 1 <1-bit, char>
            enc = bitarray('1') + h_code[ord(text[i])]
            i += 1
        n_format += 1
        data_bits += enc
    bits += elias_code(n_format)
    bits += data_bits
    return bits


if __name__ == '__main__':
    text_fp, window, lookahead = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    text = read_file(text_fp)
    bits = compress_lzss(text, window, lookahead)
    with open('./output_encoder_lzss.bin', 'wb') as bin_file:
        bits.tofile(bin_file)  # automatically pads if bits are not a multiple of 8
