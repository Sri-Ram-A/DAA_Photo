import cv2
import numpy as np
from scipy.fftpack import dct
from  . import huffman,binary_tree
from loguru import logger
import pickle

TREE_PKL_FILE_LOC="tree.pkl"

def dct2(img):
    return dct(dct(img.T, norm='ortho').T, norm='ortho')

def generate_phash(img, hash_size=8):
    resize_dim = hash_size
    # 1.  preprocess image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (resize_dim, resize_dim))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.float32(img)
    # 2. Compute 2D DCT
    coeffs = dct2(img)
    # 3. Flatten and ignore DC (first) coefficient
    ac_coeffs = coeffs.flatten()[1:]
    median_val = np.median(ac_coeffs)
    # 4. Binarize and convert to hash
    binary_matrix = coeffs >= median_val
    binary_str = ''.join(binary_matrix.flatten().astype(int).astype(str))
    hex_hash = hex(int(binary_str, 2))[2:]  # strip '0x'
    return hex_hash

# b , b_cts means b_channel and b_code_to_symbol
def image_encoding(img):
    b , g , r  = cv2.split(img)
    b_bitstream , b_cts = huffman.compress_image(b)
    g_bitstream , g_cts = huffman.compress_image(g)
    r_bitstream , r_cts = huffman.compress_image(r)
    logger.success("✅ Successfully encoded image — Blue channel bitstream length:", len(b_bitstream))
    return {
        "b_bitstream": b_bitstream,
        "g_bitstream": g_bitstream,
        "r_bitstream": r_bitstream,
        "b_cts": b_cts,
        "g_cts": g_cts,
        "r_cts": r_cts,
        "shape": b.shape
    }

def image_decoding(b_bitstream , g_bitstream , r_bitstream , b_cts, g_cts, r_cts,shape):
    b  = huffman.decompress_image(b_bitstream , b_cts, shape)
    g  = huffman.decompress_image(g_bitstream , g_cts, shape)
    r  = huffman.decompress_image(r_bitstream , r_cts, shape)
    return cv2.merge([b , g , r])

def save_tree(tree, filename=TREE_PKL_FILE_LOC):
    with open(filename, "wb") as f:
        pickle.dump(tree, f)
    logger.info("✅ Tree saved to file!")

def load_tree(filename=TREE_PKL_FILE_LOC): 
    try:
        with open(filename, "rb") as f:
            tree = pickle.load(f)
        logger.success("✅ Tree loaded from file!")
        return tree
    except FileNotFoundError:
        logger.error("⚠️ Tree file not found. Creating new tree.")
        return binary_tree.BinarySearchTree()