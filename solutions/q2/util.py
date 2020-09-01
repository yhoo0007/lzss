import heapq
import sys, inspect
from bitarray import bitarray, util


def read_file(fp):
    '''
    Reads a file and returns its content as a string.
    '''
    lines = []
    with open(fp) as file:
        for line in file:
            lines.append(line)
    return ''.join(lines)


def reverse_bits(n): 
    rev = 0
    while n > 0: 
        rev = rev << 1
        if n & 1 == 1:
            rev ^= 1
        n >>= 1
    return rev 


def huffman_code(freq_map):
    '''
    Calculates the Huffman code given a frequency map.
    
    '''
    class Node(object):
        def __init__(self, symbol, freq):
            self.symbol = symbol
            self.freq = freq

        def __lt__(self, other):
            if self.freq == other.freq:
                return len(self.symbol) < len(other.symbol)
            return self.freq < other.freq
    
    # heapify frequency map
    min_heap = [Node(symbol, freq) for symbol, freq in freq_map]
    heapq.heapify(min_heap)

    # initialize encoding table
    encoding = [None] * 128

    # handle case where starting heap has only 1 item
    if len(min_heap) == 1:
        encoding[ord(min_heap[0].symbol)] = bitarray('0')

    # merge nodes until we can merge no more
    while len(min_heap) > 1:
        # merge the two smallest nodes
        min_1 = heapq.heappop(min_heap)
        min_2 = heapq.heappop(min_heap)
        merged_node = Node(min_1.symbol + min_2.symbol, min_1.freq + min_2.freq)
        heapq.heappush(min_heap, merged_node)
        for c in min_1.symbol:  # append 0 to each char encoding in min_1
            index = ord(c)
            code = encoding[index]
            encoding[index] = bitarray('0') if code is None else bitarray('0') + code
        for c in min_2.symbol:  # append 1 to each char encoding in min_2
            index = ord(c)
            code = encoding[index]
            encoding[index] = bitarray('1') if code is None else bitarray('1') + code
    return encoding


def elias_code(number):
    '''
    Calculates the Elias omega code for the given positive integer.
    number: The number whose Elias code is calculated.
    Time:   O(log n)
    Space:  O(n)
        where:
        n = number of bits in 'number'
    '''
    if number == 0:
        return util.int2ba(0)
    code = number
    code_length = number.bit_length()
    prepend_n = code_length - 1
    while prepend_n > 0:
        prepend_mask = prepend_n << code_length
        prepend_mask_length = prepend_mask.bit_length()
        prepend_mask ^= 1 << (prepend_mask_length - 1)
        code |= prepend_mask
        code_length = prepend_mask_length
        prepend_n = prepend_n.bit_length() - 1
    return util.int2ba(code, code_length)


if __name__ == '__main__':
    pass
