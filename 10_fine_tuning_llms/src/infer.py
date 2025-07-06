from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("lora-tinyllama")
tokenizer = AutoTokenizer.from_pretrained("lora-tinyllama")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = "### Instruction:\nTranslate 'Good night' to French.\n\n### Response:"
result = pipe(prompt, max_new_tokens=50)
print(result[0]["generated_text"])