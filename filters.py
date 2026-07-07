import cv2
import numpy as np
from advanced_forgery.config import NLM_H, BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE, MASK_QUANTILE

def edge_preserving_denoise(img: np.ndarray) -> np.ndarray:
    img_u8 = np.clip(img * 255.0, 0, 255).astype(np.uint8)
    nlm = cv2.fastNlMeansDenoisingColored(img_u8, None, h=NLM_H, hColor=NLM_H, templateWindowSize=7, searchWindowSize=21)
    bil = cv2.bilateralFilter(nlm, d=BILATERAL_D, sigmaColor=BILATERAL_SIGMA_COLOR, sigmaSpace=BILATERAL_SIGMA_SPACE)
    return bil.astype(np.float32) / 255.0

def compute_hvs_texture_mask(img: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor((img * 255.0).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    mean = cv2.blur(gray, (5, 5))
    std = np.sqrt(np.clip(cv2.blur(gray**2, (5, 5)) - mean**2, 0, None))
    # Full-range mask (no floor) to maximize signal injection
    q = np.quantile(std, MASK_QUANTILE)
    mask = np.clip(std / (q + 1e-6), 0.0, 1.0)
    return np.expand_dims(mask, axis=2)