├── advanced_forgery/
│   ├── __init__.py
│   ├── config.py         # Hyperparameters, adaptive group alphas, and tuning operators
│   ├── filters.py        # Sequential NLM/Bilateral denoiser & HVS texture masking
│   ├── pipeline.py       # Core template extraction, sharpening, and injection loops
│   └── create_zip.py     # Utility to package final output without subfolders
├── Dataset.zip           # (Or extracted 'Dataset/' folder containing clean/watermarked images)
├── task_template.py # Master execution script
└── submission.py         # Evaluation server transmission script

Folder structure is important for producing same results

run 
