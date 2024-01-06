import assembly_to_qiskit
import os
from openai import AzureOpenAI
import json

def query_chatGPT(prompt):
	secrets = None
	with open('openai_secrets.txt', 'r') as file:
		secrets = json.loads(file.readline())


	client = AzureOpenAI(
		api_key = secrets['api_key'],  
		api_version = "2023-05-15",
		azure_endpoint = secrets['endpoint']
	)

	response = client.chat.completions.create(
		model=secrets['azure_oai_model'],
		messages=[
			{"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
			{"role": "user", "content": prompt}
		]
	)

	return response.choices[0].message.content


if __name__ == '__main__':
	print(query_chatGPT('tell me a fact'))










