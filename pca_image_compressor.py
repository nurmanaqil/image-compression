# pca_image_compressor.py (Final Version)

from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
import time
import os
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse

def load_image(image_path):
    """
    Load an image as a NumPy array in RGB format.
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        return np.array(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def calculate_psnr(original_image, compressed_image):
    """
    Calculate PSNR (Peak Signal-to-Noise Ratio) between two images.
    """
    original_float = original_image.astype(float)
    compressed_float = compressed_image.astype(float)
    mse_val = np.mean((original_float - compressed_float) ** 2)
    if mse_val == 0:
        return 100  # Identical images
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse_val))

def apply_pca_compression(image_array, compression_value, compression_type):
    """
    Apply PCA compression to an image.
    """
    if image_array is None:
        return None, 0, 0, 0, 0, 0, 0, "Error: Image array is None."

    height, width, channels = image_array.shape
    compressed_channels = []
    start_time = time.time()

    if compression_type == 'percentage':
        try:
            compression_percentage = float(compression_value)
            if not (0 <= compression_percentage <= 100):
                return None, 0, 0, 0, 0, 0, 0, "Compression percentage must be between 0 and 100."
            percentage_to_retain = 100.0 - compression_percentage
            n_components = max(1, int(np.ceil(min(height, width) * (percentage_to_retain / 100.0))))
        except ValueError:
            return None, 0, 0, 0, 0, 0, 0, "Invalid percentage value."
    elif compression_type == 'fixed':
        try:
            n_components = max(1, int(compression_value))
        except ValueError:
            return None, 0, 0, 0, 0, 0, 0, "Invalid fixed components value."
    else:
        return None, 0, 0, 0, 0, 0, 0, "Invalid compression type specified."

    n_components = min(n_components, min(height, width))
    explained_variances = []

    for i in range(channels):
        channel = image_array[:, :, i]
        mean_channel = np.mean(channel)
        centered = channel - mean_channel
        pca = PCA(n_components=n_components)
        transformed = pca.fit_transform(centered)
        reconstructed = pca.inverse_transform(transformed) + mean_channel
        compressed_channels.append(reconstructed)
        explained_variances.append(np.sum(pca.explained_variance_ratio_))

    compressed_image = np.stack(compressed_channels, axis=-1)
    compressed_image = np.clip(compressed_image, 0, 255).astype(np.uint8)

    runtime = time.time() - start_time
    info_retained = np.mean(explained_variances) * 100

    original_float = image_array.astype(float) / 255.0
    compressed_float = compressed_image.astype(float) / 255.0

    ssim_val = ssim(original_float, compressed_float, data_range=1, channel_axis=-1)
    mse_val = mse(original_float, compressed_float)
    psnr_val = calculate_psnr(image_array, compressed_image)
    visual_degradation = (1 - ssim_val) * 100

    return compressed_image, runtime, info_retained, visual_degradation, ssim_val, mse_val, psnr_val, None

def save_image(image_array, output_path):
    """
    Save a NumPy array as an image with compression if applicable.
    """
    try:
        img = Image.fromarray(image_array)
        file_ext = os.path.splitext(output_path)[1].lower()

        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        if file_ext in ['.jpg', '.jpeg']:
            img.save(output_path, quality=40, optimize=True)
        elif file_ext == '.webp':
            img.save(output_path, quality=40)
        else:
            img.save(output_path)

        if os.path.exists(output_path):
            file_size_kb = os.path.getsize(output_path) / 1024
            print(f"[INFO] Compressed image saved: {output_path}, size: {file_size_kb:.2f} KB")
        else:
            print(f"[WARNING] Compressed image file not found after saving: {output_path}")

        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False