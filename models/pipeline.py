from llm import generate_answer
from search import search
import os
import sys

# Ensure src directory is in sys.path for direct script execution
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_pipeline(question, top_k=5):

    print("\nSearching legal documents...")

    results = search(question, top_k=top_k)

    print(f"Found {len(results)} relevant legal chunks.")

    answer = generate_answer(question, results)

    return answer, results


def main():

    print("======================================")
    print("      AI LEGAL ASSISTANT")
    print("======================================")

    while True:

        question = input("\nEnter your legal question (or 'quit' to exit): ")

        if question.strip().lower() == "quit":
            print("Exiting...")
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        try:
            answer, results = run_pipeline(question)

            print("\n======================================")
            print("LEGAL INFORMATION")
            print("======================================")

            print(answer)

            print("\n======================================")
            print("SOURCES")
            print("======================================")

            for i, result in enumerate(results, start=1):
                print(
                    f"{i}. "
                    f"{result.get('act', 'Unknown')} | "
                    f"Section: {result.get('section', 'Unknown')} | "
                    f"Page: {result.get('page', 'Unknown')}"
                )
        except Exception as e:
            print(f"\n[Error running pipeline]: {e}")


if __name__ == "__main__":
    main()
