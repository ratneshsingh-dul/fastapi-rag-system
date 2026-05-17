from transformers import pipeline


class LocalLLM:

    def __init__(self):

        print("Loading local LLM...")

        self.pipe = pipeline(
            "text-generation",
            model="distilgpt2",
        )

        print("Local LLM loaded!")

    def generate(
        self,
        query,
        context_chunks,
    ):

        context = "\n".join(
            [
                chunk["text"]
                for chunk in context_chunks
            ]
        )

        prompt = f"""
Context:
{context}

Question:
{query}

Answer:
"""

        result = self.pipe(
            prompt,
            max_new_tokens=100,
            truncation=True,
        )

        generated_text = result[0]["generated_text"]

        answer = generated_text.split(
            "Answer:"
        )[-1].strip()

        return answer


llm = LocalLLM()


def get_llm():

    return llm