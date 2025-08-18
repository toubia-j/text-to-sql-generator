import os
MODEL_NAME = "Salesforce/codet5-small"

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "spider")  # local cached dataset

TOKENIZED_DATASET_PATH = "data/tokenized_dataset"

# Tokenization parameters
MAX_INPUT_LENGTH = 128
MAX_TARGET_LENGTH = 128
PADDING = "max_length"
TRUNCATION = True


# Training settings
BATCH_SIZE = 8
LEARNING_RATE = 5e-5
EPOCHS = 3

# Output / checkpoints
OUTPUT_DIR = "checkpoints/codet5_finetuned"
