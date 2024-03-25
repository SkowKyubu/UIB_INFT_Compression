import os
import struct


def create_dictionary():
    # Preparing the dictionary :
    minuscule = [chr(i+97) for i in range(0, 26)]
    majuscule = [chr(i+65) for i in range(0, 26)]
    norwegian_letters_and_space = [chr(198), chr(216), chr(197), chr(230), chr(248), chr(229), chr(32)]
    characters = minuscule + majuscule + norwegian_letters_and_space
    dictionary_size = len(characters)
    return {characters[i]: i for i in range(0, dictionary_size)}


def lzw_compression(file_name):
    """compress a txt file in a lzw file"""
    file_name_without_extension, _ = os.path.splitext(file_name)
    file = open(file_name, "r", encoding="utf-8")
    data = file.read()
    dictionary = create_dictionary()

    str = ""
    output = []
    dictionary_size = len(dictionary)

    for symbol in data:
        new_symbol = str + symbol
        if new_symbol in dictionary:
            str = new_symbol
        else:
            output.append(dictionary[str])
            dictionary[new_symbol] = dictionary_size
            dictionary_size += 1
            str = symbol
    if str:
        output.append(dictionary[str])
    # writing to a compressed file:
    compressed_file_name = file_name_without_extension + ".lzw"
    with open(compressed_file_name, "wb") as compressed_file:
        for code in output:
            compressed_file.write(code.to_bytes(2, byteorder='big'))


def lzw_decompress(file_name):
    """decompress the lzw file"""
    file_name_without_extension, _ = os.path.splitext(file_name)
    dictionary = create_dictionary()
    dictionary = {v: k for k, v in dictionary .items()}
    compressed_data = []
    decompressed_data = ""
    next_code = len(dictionary)
    str = ""
    file = open(file_name, "rb")
    while True:
        rec = file.read(2)
        if len(rec) != 2:
            break
        (data,) = struct.unpack('>H', rec)
        compressed_data.append(data)

    for code in compressed_data:
        if code not in dictionary:
            dictionary[code] = str + str[0]
        decompressed_data += dictionary[code]
        if len(str) != 0:
            dictionary[next_code] = str + dictionary[code][0]
            next_code += 1
        str = dictionary[code]

    with open(file_name_without_extension + "_output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(decompressed_data)
