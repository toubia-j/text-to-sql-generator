
import torch

def save_model(model, tokenizer, output_dir):
    """Save the trained model and tokenizer."""
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

def compute_accuracy(preds, labels):
    """Compute accuracy ignoring padding tokens."""
    preds = torch.argmax(preds, dim=-1)
    mask = labels != -100  # Assuming -100 is used for ignored tokens
    correct = (preds == labels) & mask
    return correct.sum().item() / mask.sum().item()
