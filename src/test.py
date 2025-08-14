from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Path to your trained checkpoint
checkpoint_path = "checkpoints/codet5_finetuned//checkpoint-2625"


tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint_path)

# Example input question
question = "How many customers have placed more than 5 orders?"

# Tokenize input
inputs = tokenizer(
    question,
    return_tensors="pt",
    padding=True,
    truncation=True,
    max_length=128
)

# Generate SQL query
output_ids = model.generate(
    **inputs,
    max_length=128,
    num_beams=4,
    early_stopping=True
)

# Decode generated SQL
generated_sql = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Generated SQL:", generated_sql)
