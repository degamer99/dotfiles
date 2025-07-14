# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Kumshe/t5-small-finetuned-hausa-to-english")
model = AutoModelForSeq2SeqLM.from_pretrained("Kumshe/t5-small-finetuned-hausa-to-english")
tokenizer.save_pretrained("./tokenizer/hausa")
model.save_pretrained("./model/hausa")
