import sys
from bitarray import bitarray, util


def read_elias(bits, start_index):
    '''
    Reads an Elias Omega encoded integer from the given bits starting at the given index. Returns
    the decoded integer and the index after reading. This function modifies the given bit array.
        bits:           Array of bits to read from.
        start_index:    Index to start reading.
    '''
    length = 1
    index = start_index
    while bits[index] == 0:  # read length components
        bits[index] = not bits[index]  # flip left-most bit
        end_index = index + length
        length = util.ba2int(bits[index:end_index]) + 1
        index = end_index
    end_index = index + length
    n = util.ba2int(bits[index:end_index])
    return n, end_index


def read_char_enc(bits, start_index):
    '''
    Reads encoded character information from the given bits and returns the character, its Huffman 
    code, and the index after reading. Character information should have been encoded in the form
    <7-bit ASCII code><length of huffmancode><huffman code>.
        bits:           Array of bits to read from.
        start_index:    Index to start reading.
    '''
    index = start_index + 7
    char = util.ba2int(bits[start_index:index])
    hcode_len, index = read_elias(bits, index)
    hcode = bits[index:index + hcode_len]
    index += hcode_len
    return char, hcode, index


def read_hcode(bits, start_index, ih_code):
    '''
    Reads a Huffman code encoded character from the given bits and returns the character and the 
    index after reading.
        bits:           Array of bits to read from.
        start_index:    Index to start reading.
        ih_code:        Binary tree representing the Huffman codes.
    '''
    index = start_index
    n = bits.length()
    node = ih_code
    while index < n and not hasattr(node, 'char'):
        node = node.child[bits[index]]
        index += 1
    return node.char, index


def decompress_lzss(bits):
    '''
    Decompresses the given LZSS compressed bits and returns the resulting string.
        bits:   Array of bits representing LZSS compressed information.
    '''
    class Node(object):
        def __init__(self):
            self.child = [None, None]

    # decode header
    unique, index = read_elias(bits, 0)  # get number of unique characters
    ih_code = Node()
    for i in range(unique):  # get each character
        char, hcode, index = read_char_enc(bits, index)
        node = ih_code
        for bit in hcode:
            if node.child[bit] is None:
                node.child[bit] = Node()
            node = node.child[bit]
        node.char = char
    
    # decode data
    n_format, index = read_elias(bits, index)  # get number of encodings
    decoded = []
    for i in range(n_format):  # decode each encoding
        if bits[index] == 0:  # format 0 <0-bit, offset, length>
            index += 1  # skip format bit
            offset, index = read_elias(bits, index)
            length, index = read_elias(bits, index)
            for j in range(len(decoded) - offset, len(decoded) - offset + length):
                decoded.append(decoded[j])
        else:  # format 1 <1-bit, char>
            index += 1  # skip format bit
            char, index = read_hcode(bits, index, ih_code)
            decoded.append(chr(char))
    return ''.join(decoded)


if __name__ == '__main__':
    file_fp = sys.argv[1]
    with open(file_fp, 'rb') as bin_file:
        bits = bitarray()
        bits.fromfile(bin_file)
    text = decompress_lzss(bits)
    with open('./output_decoder_lzss.txt', 'w') as output_file:
        output_file.write(text)
