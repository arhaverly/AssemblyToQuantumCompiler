import os
from openai import AzureOpenAI
import json
import sys
import io
import tiktoken

import assembly_to_qiskit


unsolved_problems = [
    "Boolean Satisfiability",
    # "Set Cover",
    # "Independent Set",
    # "Quadratic Assignment",
    # "3D-Matching",
    # "Bandwidth Minimization",
    # "Feedback Vertex Set",
    # "Feedback Arc Set",
    # "Closest String",
    # "Hitting Set",
    # "Minimum Vertex Coloring",
    # "Hypergraph Coloring",
    # "Clique Cover",
    # "Subset Sum",
    # "Graph Isomorphism",
    # "Maximum Independent Set",
    # "Hamiltonian Cycle",
    # "Integer Linear Programming",
    # "Bin Packing",
    # "Minimum Edge Dominating Set",
    # "Minimum Clique Cover",
    # "Maximum k-Vertex Cover",
    # "Minimum Edge Coloring",
    # "Weighted Set Packing",
    # "Shortest Common Supersequence",
    # "Longest Increasing Subsequence",
    # "RNA Folding",
    # "Maximum Network Flow",
    # "Minimum Multicut",
    # "Frequent Itemset Mining",
    # "Capacitated Facility Location",
    # "Graph Homomorphism",
    # "Disjoint Paths",
    # "Graph Edit Distance",
    # "Maximum Coverage",
    # "Minimum k-Cut",
    # "Maximum k-Cut",
    # "Constrained Maximum Cut",
    # "Minimum Bisection",
    # "Betweenness Centrality",
    # "k-Center",
    # "k-Median",
    # "Geometric Set Cover",
    # "Maximum Clique Dynamic Programming",
    # "Vehicle Routing",
    # "Prize-Collecting Steiner Tree",
    # "Maximum Common Subgraph",
    # "Longest Common Subsequence",
    # "Multidimensional Knapsack",
    # "Quadratic Knapsack",
    # "Multiple Sequence Alignment",
    # "Exact Set Cover by Pairs",
    # "Number Partitioning",
    # "Constrained Satisfiability",
    # "Maximum Edge Clique Partition",
    # "3D Bin Packing",
    # "Graph Partitioning",
    # "Project Scheduling",
    # "Cyclic Job Shop Scheduling",
    # "Maximum Directed Cut",
    # "Quadratic Programming",
    # "Maximum Dispersion",
    # "Metric k-Median",
    # "Weighted Feedback Arc Set",
    # "Weighted Feedback Vertex Set",
    # "Maximum Leaf Spanning Tree",
    # "Constrained Forest",
    # "Maximum Internal Spanning Tree",
    # "Maximum Induced Forest",
    # "Maximum Cutwidth",
    # "Hypergraph Matching",
    # "3-Partition",
    # "k-Partition",
    # "Graph Realization",
    # "Reachability",
    # "Register Allocation",
    # "Instruction Scheduling",
    # "Quadratic Assignment",
    # "Sparsest Cut",
    # "Minimum-Coloring Extension",
    # "Independent Dominating Set",
    # "Connected Dominating Set",
    # "Maximum Balanced Cut",
    # "Minimum Multiway Cut",
    # "Maximum Concurrent Flow",
    # "Node Capacitated Cut",
    # "Capacitated k-Center",
    # "Maximum Induced Matching",
    # "Chromatic Index",
    # "Minimum Maximal Matching",
    # "Maximum k-Colorable Subgraph",
    # "Feedback Set",
    # "Edge Chromatic Number",
    # "Minimum Degree Spanning Tree",
    # "Minimum Fill-In",
    # "Maximum k-Intersecting Family",
    # "Maximum Asymmetric Traveling Salesman",
    # "Maximum Concurrent Multicommodity Flow",
    # "Maximum Acyclic Subgraph",
    # "Maximum k-Set Packing",
    # "Maximum Balanced Biclique",
    # "Graph Powers",
    # "Pathwidth",
    # "Bandwidth",
    # "Treewidth",
    # "Cutwidth",
    # "Graph Augmentation",
    # "Topological Ordering",
    # "Network Design",
    # "Minimum Feedback Arc Set in Tournaments",
    # "Degree Sequence",
    # "Boxicity",
    # "Maximum k-Internal Spanning Tree",
    # "Maximum k-Dominating Set",
    # "Maximum k-Cutwidth",
    # "Minimum Clique Partition",
    # "Generalized Maximum Cut",
    # "Multicut in Trees",
    # "Tree Decomposition",
    # "Perfect Elimination Ordering",
    # "Maximum k-Tree Decomposition",
    # "Connected k-Subgraph",
    # "Maximum Simultaneous Cuts",
    # "Metric k-Center",
    # "Vertex k-Cut",
    # "Multiple Depot Vehicle Routing",
    # "Graph Bandwidth Minimization",
    # "Graph Diameter Minimization",
    # "Longest Common Substring",
    # "Maximum Monotone Subsequence",
    # "k-Dimensional Matching",
    # "Minimum Maximum Degree Spanning Tree",
    # "Set Packing",
    # "Graph Bisection Width Minimization",
    # "Geometric Maximum Coverage",
    # "Geometric k-Median",
    # "Maximum Acyclic Induced Subgraph",
    # "Total Dominating Set",
    # "k-Connected Spanning Subgraph",
    # "Hamiltonian Completion",
    # "Oriented Coloring",
    # "Maximum Induced Acyclic Subgraph",
    # "Minimum Equivalent Digraph",
    # "Maximum Scattering",
    # "Min-Max k-Cut",
    # "Minimum Equivalent Graph",
    # "Shortest Common Non-Subsequence",
    # "Generalized Maximum Flow",
    # "Minimum Sum Coloring",
    # "Chromatic Sum",
    # "Capacitated Vehicle Routing",
    # "Job Shop Scheduling with Delays",
    # "Knapsack with Conflicts",
    # "All-Pairs Shortest Paths",
    # "Maximum Balanced Induced Subgraph",
    # "Degree-Constrained Subgraph",
    # "Node-Weighted Steiner Tree",
    # "k-Way Cut",
    # "Bandwidth Allocation",
    # "Maximum Generalized Assignment",
    # "Constrained Graph Partitioning",
    # "Generalized k-Center",
    # "Maximum k-Colorable Induced Subgraph",
    # "Edge-Weighted k-Subgraph",
    # "Node-Weighted k-Median",
    # "Node-Weighted k-Center",
    # "Generalized k-Median",
    # "Minimum Node-Weighted k-Cut",
    # "Minimum Edge-Weighted k-Cut",
    # "Maximum k-Dimensional Matching",
    # "Degree-Constrained Minimum Spanning Tree",
    # "Vertex-Weighted k-Center",
    # "Vertex-Weighted k-Median",
    # "Maximum Induced Planar Subgraph",
    # "Balanced Graph Partitioning",
    # "Fixed-Size k-Cut",
    # "Maximum Edge Biclique",
    # "Minimum Vertex Biclique Cover",
    # "Disjoint Set Cover",
    # "Graph Motif",
    # "Hypergraph Vertex Cover",
    # "Planar 3-SAT",
    # "Integer Partition",
    # "Token Swapping",
    # "Maximum Agreement Subtree",
    # "Edge Dominating Set",
    # "Minimum Common Supersequence",
    # "Maximum k-Intersection",
    # "Weighted k-Coloring",
    # "Fixed-Size Edge Cut",
    # "Maximum k-Colorable Subgraph with Given Degree Sequence",
    # "Subgraph Isomorphism with Edge Contractions",
    # "Approximate Graph Coloring",
    # "Probabilistic Maximum Satisfiability",
    # "Resource Constrained Scheduling",
    # "Minimum Test Set",
    # "Weighted Maximum Cut with Node Weights",
    # "Connected Vertex Cover",
    # "Fixed-Cardinality Minimum Vertex Cover",
    # "Ordered Maximum Induced Forest",
    # "Maximum Acyclic Subgraph with Vertex Weights",
    # "Capacitated Minimum Spanning Tree",
    # "Constrained Minimum Spanning Tree",
    # "Maximum Internal k-Arborescence",
    # "Maximum Simultaneous Planar Graph Embeddings",
    # "Maximum Induced Subgraph with Color Constraints",
    # "Minimum Edge Coloring with Capacity Constraints",
    # "Maximum Weight Perfect Matching in Non-bipartite Graphs",
    # "k-Internal Spanning Tree",
    # "Maximum Common Induced Bipartite Subgraph",
    # "Maximum Induced Matched Subgraph",
    # "Maximum k-Leaf Spanning Tree",
    # "Minimum k-Leaf Spanning Tree",
    # "Robust Network Design",
    # "Maximum Multi-commodity Flow",
    # "Minimum k-Cut with Capacity Constraints",
    # "Node-Weighted Maximum Cut",
    # "Partial Vertex Cover",
    # "Minimum Node-Weighted Multicut",
    # "Fixed-Size k-Way Cut",
    # "Weighted k-Partition",
    # "Maximum Induced Subgraph with Color Symmetry",
    # "Minimum Feedback Vertex Set with Vertex Weights",
    # "Weighted Clique Partitioning",
    # "Maximum Disjoint Induced Paths",
    # "Maximum Simultaneous Acyclic Subgraphs",
    # "Cyclic Scheduling",
    # "Minimum Maximum Degree Spanning Tree"
]



system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 2000
token_limit = 4096



def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens






def create_prompt(problem):
    return f'''
There are values stored in R0, R1, and R2 that cannot be changed. Decide what these values represent then write ARM assembly code without loops using the following instructions to decide if these values are a valid solution to the {problem} problem.

[ADC, ADD, AND, BIC, CMN, CMP, EOR, LSL, LSR, MOV, MRS, MSR, MVN, ORR, RSB, RSC, SBC, STR, SUB, TEQ, TST]

Store the value in the R5 register. Setting the value to 1 indicates that the values in R0, R1, and R2 are a solution, and 0 is NOT a solution. The largest number allowed for your example is 3.

The computer running this program is very limited so be efficient.

Assume this code is going to be run directly on the ARM processor, so all immediate values must be written out.

Unbreakable requirements:
1. Do not use [MUL, MLA, B, BEQ, BNE, MOVEQ, MOVNE, ADDS, ADDNE, ADDEQ, ANDS, ORREQ, ORRNE, CMPEQ, CMPNE, CMEQ, CMNE, SUBS].
2. Each register can only be used once
3. A register cannot be used twice in an instruction.
4. ONLY use the instructions above that you are allowed to use.
5. Branches, loops, and labels are not allowed.
6. Signify when the assembly code begins and ends using "START_ASSEMBLY" and "END_ASSEMBLY" rather than putting it in a code block.
7. Labels are not allowed.
8. Registers must resemble the form R0, R1, etc.
9. Comments are denoted by the ';' character.
10. Immediate values cannot be in hex or binary.
11. The ZERO PSR flag can only be set once.
'''

# I want there to be fewer than 5 instructions in this code.
# The largest number allowed for your example is 3.





def query_chatGPT(prompt, conversation):
    secrets = None
    with open('openai_secrets.txt', 'r') as file:
        secrets = json.loads(file.readline())


    client = AzureOpenAI(
        api_key = secrets['api_key'],
        api_version = "2023-05-15",
        azure_endpoint = secrets['endpoint']
    )


    conversation.append({"role": "user", "content": prompt})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1]
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens
    )


    conversation.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content



preamble = '''{"register_size": 1, "run": true, "display": true}
HAD R0
HAD R1
HAD R2

ORACLE

'''

postamble = '''

END_ORACLE

TGT R5

REVERSE_ORACLE

DIF {R0, R1, R2}

STR CR0, R0
STR CR1, R1
STR CR2, R2

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



def write_paper(problem, paper_filename, algorithm_conversation, assembly_filename):
    print(f'\n\n\nWriting Paper: {problem}\n\n\n')

    paper_conversation = []
    paper_conversation.append(system_message)

    with open(paper_filename, 'w') as paper:

        prompt = f"""I'm writing an IEEE PhD level research paper on using Grover's Algorithm to solve the {problem} problem. I've already written the algorithm.

Can you please provide the abstract and introduction for this paper?

Please write 500 words total formatted in LaTeX. Assume this is going to be directly compiled and submitted to the journal, so don't give any preamble or incomplete sections.

Don't include the bibliography or '\\end{{document}}'
        """

        paper.write(query_chatGPT(prompt, paper_conversation))

        paper.write('\n\n')


        prompt = f"""Great work! Can you please write 500 words to explain what the values in R0 and R1 represent as well as the rest of your algorithm?

Please format your response in LaTeX sections that I can copy/paste into an existing LaTeX document.

This is for a PhD level research paper.

Assume that the abstract, introduction, and conclusion are already handled for you.

Don't include the bibliography or '\\end{{document}}'
        """

        paper.write(query_chatGPT(prompt, algorithm_conversation))

        paper.write('\n\n')

        paper.write(f"""

\\section{{Implementation}}

The following program is an implementation of the above description. The created circuit is shown in Figure \\ref{{fig:{problem.replace(' ', '_')}}}:

\\begin{{lstlisting}}

""")

        with open(assembly_filename, 'r') as assembly:
            for line in assembly:
                paper.write(line)


        paper.write(f"""
\\end{{lstlisting}}

\\begin{{figure}}[htp]
    \\centering
    \\includegraphics[width=9cm]{{Figures/{problem.replace(' ', '_')}_circuit.png}}
    \\caption{{Using Grover's Algorithm to Solve the {problem} Problem}}
    \\label{{fig:{problem.replace(' ', '_')}}}
\\end{{figure}}

""")


        prompt = f"""Awesome! Now can you please provide just the conclusion so that I can copy/paste into the existing document? Don't include the bibliography or '\\end{{document}}'"""

        paper.write(query_chatGPT(prompt, paper_conversation))

        paper.write('\n\n')


def create_grovers_solution(problem):
    assembly_filename = f"assembly_programs/automatically_generated/{problem.replace(' ', '_')}.s"
    paper_filename = f"papers/{problem.replace(' ', '_')}.tex"


    for i in range(10):
        conversation = []
        conversation.append(system_message)

        prompt = create_prompt(problem)

        for j in range(2):
            try:
                response = query_chatGPT(prompt, conversation)

                create_assembly(assembly_filename, response)

                assembly_to_qiskit.run_assembly(assembly_filename)

                write_paper(problem, paper_filename, conversation, assembly_filename)

                print('\n\n\nDone!\n\n\n')


                return

            except Exception as error:
                os.remove(assembly_filename)

                error_message = str(error)
                print(error_message)
                if 'duplicate qubit arguments' in error_message:
                    prompt = 'You broke the rule that says "a register cannot be used twice in an instruction."'
                elif "'NoneType' object is not subscriptable" in error_message:
                    prompt = 'You must set the ZERO PSR flag before you reference it.'
                elif 'Invalid Instruction' in error_message:
                    prompt = 'You used an invalid instruction or you used a label (like "loop"), which isn\'t allowed. Use only these: [ADC, ADD, AND, BIC, CMN, CMP, EOR, LSL, LSR, MOV, MRS, MSR, MVN, ORR, RSB, RSC, SBC, STR, SUB, TEQ, TST]'
                else:
                    prompt = 'You broke a rule.'

                prompt += ' Try again.'

                print(f'\nAttempt {j} in restart {i}\nResponse to GPT:', prompt)




def solve_problems():
    for problem in unsolved_problems:
        create_grovers_solution(problem)




if __name__ == '__main__':
    # create_grovers_solution(' '.join(sys.argv[1:]))
    solve_problems()








