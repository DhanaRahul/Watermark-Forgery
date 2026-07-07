# src/advanced_forgery/pipeline.py
import numpy as np
import cv2
from pathlib import Path
from PIL import Image
from advanced_forgery.config import (
    GROUPS, TARGET_MAPPING, WATERMARKED_SOURCES_DIR, 
    CLEAN_TARGETS_DIR, FORGED_OUT_DIR, GROUP_ALPHAS, 
    NORM_QUANTILE, TEMPLATE_SHARPEN_FACTOR
)
from advanced_forgery.filters import edge_preserving_denoise, compute_hvs_texture_mask

def run_advanced_pipeline():
    """Runs extraction loops and outputs final altered target prints."""
    FORGED_OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("✨ Core Pipeline Initialized. Commencing adaptive frequency sequence...")
    
    base_sources = WATERMARKED_SOURCES_DIR
    base_targets = CLEAN_TARGETS_DIR

    # Nested check safeguard
    if not (base_sources / GROUPS[0]).exists() and (base_sources / "Dataset").exists():
        base_sources = base_sources / "Dataset" / "watermarked_sources"
        base_targets = base_targets.parent / "Dataset" / "clean_targets"

    for wm_group in GROUPS:
        start_idx, end_idx = TARGET_MAPPING[wm_group]
        base_alpha = GROUP_ALPHAS.get(wm_group, 0.14)
        print(f" -> Optimization Pass [{wm_group}]: Target Alpha={base_alpha}")
        
        # 1. EXTRACT TEMPLATE
        source_dir = base_sources / wm_group
        source_paths = sorted(list(source_dir.glob("*.png")), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem)
        
        residuals = []
        for src_path in source_paths:
            src_arr = np.array(Image.open(src_path).convert("RGB")).astype(np.float32) / 255.0
            residuals.append(src_arr - edge_preserving_denoise(src_arr))
            
        # Median pooling to filter background image outliers
        watermark_template = np.median(np.stack(residuals, axis=0), axis=0)
        
        # --- ENHANCEMENT: LAPLACIAN HIGH-PASS SHARPENING PASS ---
        # Sharpens the details of the watermark pattern before scaling
        blur_template = cv2.GaussianBlur(watermark_template, (3, 3), 0)
        high_pass = watermark_template - blur_template
        watermark_template = watermark_template + (TEMPLATE_SHARPEN_FACTOR * high_pass)
        
        # Zero-center and robust-scale normalize
        watermark_template -= watermark_template.mean(axis=(0, 1), keepdims=True)
        scale = np.quantile(np.abs(watermark_template), NORM_QUANTILE)
        if scale > 1e-6:
            watermark_template /= scale
            
        # 2. TARGET INJECTION
        for idx in range(start_idx, end_idx + 1):
            target_path = base_targets / f"{idx}.png"
            target_arr = np.array(Image.open(target_path).convert("RGB")).astype(np.float32) / 255.0
            
            # Dynamic embedding optimization calculation
            hvs_mask = compute_hvs_texture_mask(target_arr)
            strength_coef = np.mean(np.abs(watermark_template))
            alpha = base_alpha * (0.90 + 0.25 * np.tanh(strength_coef))
            
            # Fuse customized high-pass watermark signal
            forged_arr = target_arr + (alpha * hvs_mask * watermark_template)
            forged_output = np.clip(forged_arr * 255.0, 0, 255).astype(np.uint8)
            
            # Save flattened assets
            Image.fromarray(forged_output).save(FORGED_OUT_DIR / f"{idx}.png")

    print("🏁 Pipeline processing complete.")