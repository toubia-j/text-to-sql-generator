from transformers import AutoTokenizer
from data import *
from config import *

def tokenize_dataset(dataset):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize_function(example):
        # Inputs
        model_inputs = tokenizer(
            example["question"],
            padding=PADDING,
            truncation=TRUNCATION,
            max_length=MAX_INPUT_LENGTH
        )
        # Targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                example["query"],
                padding=PADDING,
                truncation=TRUNCATION,
                max_length=MAX_TARGET_LENGTH
            )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    return dataset.map(tokenize_function, batched=False)

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print(f"Loading Spider dataset from {DATA_DIR} ...")
    datasets = get_spider_dataset(subset_ratio=1.0)  # This should return a dict with splits

    for split_name, ds in datasets.items():
        print(f"Tokenizing {len(ds)} samples from {split_name} split...")
        tokenized_ds = tokenize_dataset(ds)

        save_path = f"data/tokenized_{split_name}"
        print(f"Saving tokenized {split_name} dataset to {save_path} ...")
        tokenized_ds.save_to_disk(save_path)

    print("Tokenization complete for all splits!")
