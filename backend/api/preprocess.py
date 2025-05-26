import cv2
import numpy as np
from scipy.fftpack import dct
from PIL import Image

def dct2(img):
    return dct(dct(img.T, norm='ortho').T, norm='ortho')

def generate_phash(image_path, hash_size=8):
    resize_dim = hash_size
    # 1. Load and preprocess image
    img = cv2.imread(image_path)
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
