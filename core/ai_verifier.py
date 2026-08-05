import math
from PIL import Image


def _dhash(image, hash_size=8):
    """
    Computes difference hash (dHash) for an image.
    """
    # Resize to (hash_size + 1, hash_size) and convert to grayscale
    img = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(img.getdata())

    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = pixels[row * (hash_size + 1) + col]
            pixel_right = pixels[row * (hash_size + 1) + col + 1]
            difference.append(pixel_left > pixel_right)

    # Convert binary array to integer hash
    decimal_value = 0
    for bit in difference:
        decimal_value = (decimal_value << 1) | bit
    return decimal_value


def _hamming_distance(hash1, hash2, bit_length=64):
    """
    Calculates Hamming distance between two integer hashes.
    """
    x = hash1 ^ hash2
    return bin(x).count('1')


def _color_histogram(image, bins_per_channel=4):
    """
    Computes a normalized color histogram vector for an RGB image.
    """
    img = image.convert('RGB').resize((128, 128), Image.Resampling.LANCZOS)
    histogram = [0] * (bins_per_channel ** 3)

    shift = 8 - int(math.log2(bins_per_channel))
    for r, g, b in img.getdata():
        r_idx = r >> shift
        g_idx = g >> shift
        b_idx = b >> shift
        idx = (r_idx * bins_per_channel * bins_per_channel) + (g_idx * bins_per_channel) + b_idx
        histogram[idx] += 1

    total = sum(histogram) or 1
    return [c / total for c in histogram]


def _cosine_similarity(vec1, vec2):
    """
    Computes cosine similarity between two numerical vectors.
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = math.sqrt(sum(a * a for a in vec1))
    norm_b = math.sqrt(sum(b * b for b in vec2))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def verify_product_image_match(uploaded_file, reference_product_image, similarity_threshold=0.32):
    """
    Compares an uploaded review image against a reference product image.
    Returns (is_match: bool, similarity_score: float).

    Uses perceptual hashing (dHash) and RGB color histogram correlation
    to verify if the uploaded photo matches the visual profile of the product.
    """
    if not reference_product_image:
        return True, 1.0

    try:
        # Open uploaded image
        uploaded_file.seek(0)
        uploaded_img = Image.open(uploaded_file)

        # Open reference product image
        if hasattr(reference_product_image, 'path'):
            ref_img = Image.open(reference_product_image.path)
        elif hasattr(reference_product_image, 'file'):
            ref_img = Image.open(reference_product_image.file)
        else:
            ref_img = Image.open(reference_product_image)

        # 1. Calculate dHash similarity
        hash_uploaded = _dhash(uploaded_img)
        hash_ref = _dhash(ref_img)
        h_dist = _hamming_distance(hash_uploaded, hash_ref)
        hash_similarity = 1.0 - (h_dist / 64.0)

        # 2. Calculate Color Histogram similarity
        hist_uploaded = _color_histogram(uploaded_img)
        hist_ref = _color_histogram(ref_img)
        color_sim = _cosine_similarity(hist_uploaded, hist_ref)

        # Combined visual score
        combined_score = (hash_similarity * 0.4) + (color_sim * 0.6)

        is_match = combined_score >= similarity_threshold
        return is_match, round(combined_score, 4)

    except Exception as e:
        # If image cannot be read or processed, treat as non-matching
        return False, 0.0
