import os
import struct
from heapq import heappush, heappop


class Node:
    def __init__(self, value, letter="", NodeLeft=None, NodeRight=None):
        """constructor"""
        self.value = value
        self.letter = letter
        self.NodeLeft = NodeLeft
        self.NodeRight = NodeRight

    def __lt__(self, Node2):
        """compare two node values"""
        return self.value < Node2.value


def is_empty(Node):
    """check if the node is empty"""
    return Node is None


def is_leaf(Node):
    """check if a node is a node"""
    return is_empty(Node.NodeLeft) and is_empty(Node.NodeRight)


def occurrence(data):
    """count the number of occurrences for each present letters in data"""
    # extract the different values:
    values_to_count = []
    occ = []
    for value in data:
        if value not in values_to_count:
            values_to_count.append(value)
    for value in values_to_count:
        number_occurrences = data.count(value)
        letter = [value, number_occurrences]
        occ.append(letter)
    return occ


def build_huffman(data):
    """build the huffman tree"""
    occ = occurrence(data)
    priority_file = []
    for element in occ:
        n = Node(element[1], element[0])
        heappush(priority_file, n)
    while len(priority_file) > 1:
        n1 = heappop(priority_file)
        n2 = heappop(priority_file)
        n3 = Node(n1.value + n2.value)
        n3.NodeLeft = n2
        n3.NodeRight = n1
        heappush(priority_file, n3)
    # Root :
    return heappop(priority_file)


def make_huffman_code(data):
    """Create the code dictionary"""
    root_node = build_huffman(data)
    dic = {}
    code_huffman(root_node, dic, "")
    return dic


def code_huffman(n, dictionary, code):
    """recursive function to create the huffman code"""
    if is_leaf(n):
        dictionary[code] = n.letter
    else:
        code_huffman(n.NodeLeft, dictionary, code + '0')
        code_huffman(n.NodeRight, dictionary, code + '1')


def code_data(data, dictionary):
    """apply the huffman code to the data"""
    output = ""
    dictionary = {v: k for k, v in dictionary.items()}
    for sample in data:
        output += dictionary[sample]

    # Convertir la chaîne de bits en une liste de bits
    bits = [output[i:i+8] for i in range(0, len(output), 8)]

    # Convertir la liste de bits en une liste d'octets
    bytes_output = bytes([int(bit, 2) for bit in bits])

    with open("huffman.bin", "wb") as file:
        file.write(bytes_output)

    return output


def decode_data(file_name, dictionary):
    """open a bin file and decode the message"""
    file_name_without_extension, _ = os.path.splitext(file_name)
    data_compress = read_data(file_name)
    decode = []
    tempo = ""
    for num in data_compress:
        tempo += num
        if tempo in dictionary.keys():
            decode.append(dictionary[tempo])
            tempo = ""
    compressed_file_name = file_name_without_extension + "_after_huffman.lzw"
    with open(compressed_file_name, "wb") as compressed_file:
        for code in decode:
            compressed_file.write(code.to_bytes(2, byteorder='big'))

    return decode


def read_data(file_name):
    """open a bin file and convert the file in a string"""
    with open(file_name, "rb") as file:
        bytes_data = file.read()
        # Convertir les octets en une chaîne binaire
        binary_data = "".join(format(byte, "08b") for byte in bytes_data)
    return binary_data


def open_file(file_name):
    """open a lzw file and create an array with the code"""
    compressed_data = []
    file = open(file_name, "rb")
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data,) = struct.unpack('>H', rec)
        compressed_data.append(data)
    return compressed_data
