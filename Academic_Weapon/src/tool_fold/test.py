from huggingface_hub import InferenceClient

client = InferenceClient(api_key="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")

messages = [
	{ "role": "user", "content": "peut tu me faire un résumer sur la cryptographie" }
]

stream = client.chat.completions.create(
    model="codellama/CodeLlama-34b-Instruct-hf",
	messages=messages, 
	temperature=0.5,
	max_tokens=5888,
	top_p=0.7,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")