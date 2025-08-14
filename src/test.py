from datasets import load_from_disk

# Paths to tokenized splits
splits = ["train", "validation"]

for split in splits:
    path = f"data/tokenized_{split}"
    print(f"\nLoading tokenized {split} dataset from {path} ...")
    
    tokenized_ds = load_from_disk(path)
    
    print(f"Number of samples in {split}: {len(tokenized_ds)}")
    
    # Print first example
    print("Example:", tokenized_ds[0])
    
    # Inspect inputs and labels
    print("Input IDs:", tokenized_ds[0]["input_ids"][:20], "...")
    print("Labels:", tokenized_ds[0]["labels"][:20], "...")
