import lzw
import Huffman

# Compress the data and save the output in a lzw file
lzw.lzw_compression("folktale.txt")

# Open the lzw file and apply the Huffman code
data = Huffman.open_file("folktale.lzw")
code_dictionary = Huffman.make_huffman_code(data)
Huffman.code_data(data, code_dictionary)  # create a bin code

# Open the bin code and decompress the data in a lzw file
Huffman.decode_data("huffman.bin", code_dictionary)

# Decompress the lzw to the original file
lzw.lzw_decompress("huffman_after_huffman.lzw")
