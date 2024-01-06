import os
from openai import AzureOpenAI
import json
import sys
import io


import assembly_to_qiskit







def create_prompt(problem):
	return f'''
There are values stored in R0 and R1 that cannot be changed. Decide what these values represent then write efficient ARM assembly code using the following instructions to decide if these values are a valid solution to the {problem} problem.

[ADC, ADD, AND, BIC, CMN, CMP, EOR, LSL, LSR, MLA, MOV, MRS, MSR, MUL, MVN, ORR, RSB, RSC, SBC, STR, SUB, TEQ, TST]

Store the value in the ZERO PSR flag. The largest number allowed for your example is 3.

Each register can only be used once.

Do not use [B, BEQ, BNE, MOVEQ, MOVNE, ADDS, ORREQ, ORRNE, CMPEQ, CMPNE, CMEQ, CMNE]. ONLY use the instructions above that you are allowed to use.

Signify when the assembly code begins and ends using "START_ASSEMBLY" and "END_ASSEMBLY" rather than putting it in a code block.

I want there to be fewer than 5 instructions in this code.
'''



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


preamble = '''{"register_size": 2}
HAD R0
HAD R1

ORACLE

'''

postamble = '''

END_ORACLE

TGT ZERO

REVERSE_ORACLE

DIF {R0, R1}

STR CR0, R0
STR CR1, R1

'''


def create_assembly(filename, gpt_response):
	in_code = False
	
	with open(filename, 'w') as file:

		file.write(preamble)

		# write oracle
		for line in gpt_response.split('\n'):
			if line == 'START_ASSEMBLY':
				in_code = True
			elif line == 'END_ASSEMBLY':
				in_code = False
			elif in_code:
				file.write(line + '\n')
			else:
				print(line)

		file.write(postamble)




if __name__ == '__main__':
	prompt = create_prompt(' '.join(sys.argv[1:]))

	response = query_chatGPT(prompt)

	filename = 'assembly_code.tmp'
	
	create_assembly(filename, response)

	assembly_to_qiskit.run_assembly(filename)










