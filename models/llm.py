import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Search multiple candidate paths for .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(project_dir)

env_candidates = [
    os.path.join(current_dir, ".env"),
    os.path.join(project_dir, ".env"),
    os.path.join(parent_dir, ".env"),
]

for env_path in env_candidates:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)

load_dotenv()  # Fallback to standard environment search


def get_llm():
    """
    Instantiate and return the Groq Chat model using GROQ_API_KEY.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not found in environment or .env file.")

    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=700,
        api_key=api_key
    )


# System prompt
SYSTEM_PROMPT = """
You are an Indian Legal Information Assistant.

Your job is to answer questions using ONLY the legal context
provided by the user.

Rules:

1. Use only the provided legal context.
2. Do not invent sections, punishments, laws or legal facts.
3. If the answer is not present in the context, say:
   "The provided legal documents do not contain enough information
   to answer this question."
4. Mention the Act name and section number when available.
5. Give a clear and simple answer.
6. Do not pretend to be a lawyer.
7. Do not provide false or unsupported legal information.
"""


def generate_answer(question, results):

    if not results:
        return "No relevant legal information was found."

    context = ""

    for i, result in enumerate(results, start=1):

        context += f"""
--- Legal Source {i} ---

Act: {result.get("act", "Unknown")}
Section: {result.get("section", "Unknown")}
Title: {result.get("title", "Unknown")}
Page: {result.get("page", "Unknown")}

Text:
{result.get("text", "")}

"""

    prompt = f"""
{SYSTEM_PROMPT}

LEGAL CONTEXT:
{context}

USER QUESTION:
{question}

Answer the question using only the legal context above.

Give the answer in a clear format.
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content


if __name__ == "__main__":
    print("Testing LLM generation with sample context...")
    sample_results = [
        {
            "act": "Bharatiya Nyaya Sanhita, 2023",
            "section": "306",
            "title": "Theft",
            "page": 89,
            "text": "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft. Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both."
        }
    ]
    response = generate_answer("What is the punishment for theft under BNS?", sample_results)
    print("\n--- Response ---")
    print(response)