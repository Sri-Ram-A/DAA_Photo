import cv2
import numpy as np
from scipy.fftpack import dct
from  . import huffman,binary_tree
from loguru import logger
import pickle
from PIL import Image, ImageOps

TREE_PKL_FILE_LOC="tree.pkl"

def dct2(img):
    return dct(dct(img.T, norm='ortho').T, norm='ortho')

def generate_phash(img, hash_size=8):
    # Convert OpenCV image to PIL Image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    
    # Define the orientations to test
    orientations = [
        ("Original", pil_img.copy()),
        ("Rotated 90", pil_img.copy().rotate(90, expand=True)),
        ("Mirrored", ImageOps.mirror(pil_img.copy()))
    ]
    
    candidate_hashes = []
    
    for name, img_obj in orientations:
        # Process each orientation
        resize_dim = hash_size * 4  
        img_resized = img_obj.resize((resize_dim, resize_dim), Image.Resampling.LANCZOS)
        img_gray = img_resized.convert("L")
        
        # Convert to numpy array for DCT
        img_array = np.array(img_gray, dtype=float)
        dct_coeffs = dct2(img_array)
        dct_reduced = dct_coeffs[:hash_size, :hash_size]
        
        # Compute hash
        ac_coeffs = dct_reduced.flatten()[1:]
        median_val = np.median(ac_coeffs)
        binary_matrix = dct_reduced >= median_val
        binary_str = ''.join(binary_matrix.flatten().astype(int).astype(str))
        hex_hash = hex(int(binary_str, 2))[2:]
        candidate_hashes.append(hex_hash)
    
    # Return the smallest hash as canonical
    return min(candidate_hashes)
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