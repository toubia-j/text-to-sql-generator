from datasets import load_from_disk
from transformers import AutoModelForSeq2SeqLM
from data import *
from config import *
from transformers import AutoTokenizer

train_dataset = load_from_disk("data/tokenized_train")
val_dataset   = load_from_disk("data/tokenized_validation")

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments

training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,
    eval_strategy="epoch",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=EPOCHS,
    predict_with_generate=True,
    logging_dir="./logs",
    logging_strategy="steps",
    logging_steps=50
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=AutoTokenizer.from_pretrained(MODEL_NAME)
)

trainer.train()

results = trainer.evaluate(val_dataset)
print(results)