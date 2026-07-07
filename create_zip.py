
import zipfile
from pathlib import Path
from advanced_forgery.config import FORGED_OUT_DIR, FINAL_ZIP_PATH, EXPECTED_COUNT

def create_clean_submission():
    """Validates structural constraints and generates flat file submission package."""
    png_files = sorted(list(FORGED_OUT_DIR.glob("*.png")), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem)
    actual_count = len(png_files)
    
    print("\n" + "="*50)
    print("PRE-FLIGHT VERIFICATION CHECKS")
    print("="*50)
    print(f"Target Dir:   {FORGED_OUT_DIR}")
    print(f"File Count:   {actual_count} / {EXPECTED_COUNT}")
    
    if actual_count != EXPECTED_COUNT:
        raise ValueError(f"Security check failure: Expected 200 assets, found {actual_count}. Fix pipeline constraints before pushing.")
        
    
    expected_names = {f"{i}.png" for i in range(1, EXPECTED_COUNT + 1)}
    actual_names = {p.name for p in png_files}
    if expected_names != actual_names:
        raise ValueError("Security check failure: Malformed naming strings detected in output array.")
        
    print("All integrity verifications passed. Packing submission file...")
    FINAL_ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    if FINAL_ZIP_PATH.exists():
        FINAL_ZIP_PATH.unlink()
        
    with zipfile.ZipFile(FINAL_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for img_path in png_files:
            
            zipf.write(img_path, arcname=img_path.name)
            
    print(f"Flat file archive compiled successfully at: {FINAL_ZIP_PATH}\n")

if __name__ == "__main__":
    create_clean_submission()