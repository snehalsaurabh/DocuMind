# backend/llm/prompt_template.py

def build_prompt(context: str, question: str) -> str:
    return f"""Based on the following context, please answer the question. 
If the answer cannot be found in the context, say so.

Context:
{context}

Question: {question}

Answer:"""