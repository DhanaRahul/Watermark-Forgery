
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = PROJECT_ROOT / "Dataset"
OUTPUT_ROOT = PROJECT_ROOT / "outputs"

WATERMARKED_SOURCES_DIR = DATASET_ROOT / "watermarked_sources"
CLEAN_TARGETS_DIR = DATASET_ROOT / "clean_targets"
FORGED_OUT_DIR = OUTPUT_ROOT / "advanced_submission_temp"
FINAL_ZIP_PATH = OUTPUT_ROOT / "submission.zip"

GROUPS = ["WM_1", "WM_2", "WM_3", "WM_4", "WM_5", "WM_6", "WM_7", "WM_8"]

TARGET_MAPPING = {
    "WM_1": (1, 25),
    "WM_2": (26, 50),
    "WM_3": (51, 75),
    "WM_4": (76, 100),
    "WM_5": (101, 125),
    "WM_6": (126, 150),
    "WM_7": (151, 175),
    "WM_8": (176, 200),
}


NLM_H = 7                    
BILATERAL_D = 7               
BILATERAL_SIGMA_COLOR = 30    
BILATERAL_SIGMA_SPACE = 30    

MASK_FLOOR = 0.20             
MASK_QUANTILE = 0.96          


GROUP_ALPHAS = {
    "WM_1": 0.13,
    "WM_2": 0.14,
    "WM_3": 0.12,  
    "WM_4": 0.15,  
    "WM_5": 0.16,  
    "WM_6": 0.13,  
    "WM_7": 0.17,  
    "WM_8": 0.12, 
}

NORM_QUANTILE = 0.995        
TEMPLATE_SHARPEN_FACTOR = 0.35 
EXPECTED_COUNT = 200