from langchain.prompts import PromptTemplate

PROMPT_TEMPLATE = """
You are a helpful assistant. Answer the question using ONLY the context provided below.
If the answer is not found in the context, respond with:
"I don't know based on this document."

Context:
{context}

Question: {question}

Answer:"""

def get_prompt():
    return PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )