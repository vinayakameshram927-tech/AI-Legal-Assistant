import os
import sys

# Ensure src directory is in sys.path for direct script execution from any directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

# Import all linked modules and functions
from build_data import build_data
from build_index import build_index
from search import search, display_results
from pipeline import run_pipeline


def main():
    base_dir = os.path.dirname(SRC_DIR)
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)

    while True:
        print("\n===================================")
        print("  AI LEGAL ASSISTANT PIPELINE")
        print("===================================")
        print("1. Process PDFs & Build Data (Extract & Chunk)")
        print("2. Build BM25 Index")
        print("3. Keyword Search (BM25 Retrieval)")
        print("4. AI Legal Assistant (Full RAG: Search + LLM Answer)")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            print("\n--- Processing PDFs and Building Data ---")
            build_data()

        elif choice == '2':
            print("\n--- Building BM25 Index ---")
            try:
                build_index()
            except Exception as e:
                print(f"[Error]: {e}")

        elif choice == '3':
            print("\n--- Search Legal Documents ---")
            question = input("\nEnter your legal question: ")
            if question.strip():
                try:
                    results = search(query=question, top_k=5)
                    display_results(results)
                except Exception as e:
                    print(f"[Error]: {e}")

        elif choice == '4':
            print("\n--- AI Legal Assistant ---")
            question = input("\nEnter your legal question: ")
            if question.strip():
                try:
                    answer, results = run_pipeline(question, top_k=5)
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
                    print(f"[Error]: {e}")

        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
