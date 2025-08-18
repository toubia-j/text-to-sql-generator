
# Tokenizer and Model

## Model

For text-to-SQL translation, this project uses the **CodeT5 small model** from Salesforce (`Salesforce/codet5-small`).  
This is a sequence-to-sequence (Seq2Seq) model designed for code understanding and generation. It is fine-tuned on the Spider dataset to translate natural language questions into SQL queries.

## Tokenizer

The **tokenizer** converts natural language questions and SQL queries into numerical token IDs that the model can process.  
It ensures proper handling of input and output sequences, including padding, truncation, and maximum sequence lengths.

## Fine-tuning

We fine-tune the model using Hugging Face's **Seq2SeqTrainer**, which handles training, evaluation, and saving the model.  
Fine-tuning allows the model to adapt from its pretrained general code knowledge to the specific text-to-SQL translation task.
