import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from database import fetch_schema

# initializing tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# loading model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

# fetching table schema
schema = fetch_schema()
columns = ", ".join(f"{key} {val}" for key, val in schema.items())

table_schema = f"CREATE TABLE properties ({columns})"

def generate_sql(question):
    input_prompt = "tables:\n" + table_schema + "\n" + "query for:" + question

    # tokenizing the input prompt
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)

    # forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)

    # decoding the output into string
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_sql