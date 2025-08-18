from datasets import load_dataset
import os

# Define local cache directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_spider_dataset(splits=("train", "validation"), subset_ratio=1.0):
    """
    Load Spider dataset splits locally, with caching in ./data.
    Returns a dict of datasets keyed by split name.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    datasets = {}
    for split in splits:
        datasets[split] = load_dataset(
            "spider",
            split=f"{split}[:{int(subset_ratio*100)}%]",
            cache_dir=DATA_DIR
        )
    return datasets

if __name__ == "__main__":
    datasets = get_spider_dataset()
    for split_name, ds in datasets.items():
        print(f"Loaded {len(ds)} samples from {split_name} split.")
        print(f"Example from {split_name}:", ds[0])
