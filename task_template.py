
import os
import zipfile
from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from advanced_forgery.config import DATASET_ROOT, EXPECTED_COUNT
from advanced_forgery.pipeline import run_advanced_pipeline
from advanced_forgery.create_zip import create_clean_submission


ZIP_FILE = "Dataset.zip"

def main():
    print("=" * 70)
    print("ADVANCED WATERMARK FORGERY ATTACK FRAMEWORK")
    print("=" * 70)

    # 1. DATASET UNPACKING PHASE
    if not DATASET_ROOT.exists():
        if not os.path.exists(ZIP_FILE):
            raise FileNotFoundError(
                f"Could not locate '{ZIP_FILE}'. Please ensure the dataset zip "
                f"is downloaded and placed in the project root folder."
            )

        print(f"Extracting raw assets from {ZIP_FILE}...")
        with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
            zip_ref.extractall(".")
        print("Extraction complete.")
    else:
        print("Dataset directories already present. Skipping unpacking phase.")

    
    print("\n⚡ Initiating Anisotropic Frequency Decomposition pipeline...")
    run_advanced_pipeline()

   
    print("\n🔒 Commencing pre-flight validation checks...")
    try:
        create_clean_submission()
        print("=" * 70)
        print("SUCCESS: Advanced forgery deployment executed perfectly!")
        print(f"Your flat submission file is ready for upload at: outputs/submission.zip")
        print("=" * 70)
    except Exception as e:
        print(f"\nPIPELINE ERROR: Validation failed during packing : {e}")
        print("Please check your input directories and dataset constraints.")
        print("=" * 70)

if __name__ == "__main__":
    main()