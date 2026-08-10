from prebuilt_agent import ask_agent
from output_formatter import print_response


def main():

    print("\n" + "=" * 80)
    print("Credit Card Management System Agent")
    print("Implementation Choice-1 : LangGraph Prebuilt ReAct Agent")
    print("=" * 80)

    while True:

        question = input("\nAsk a question (or type 'exit'): ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nGoodbye!")
            break

        try:

            response = ask_agent(question)

            tool_used = response.get(
                "tool_used",
                "Not Available"
            )

            records_found = response.get(
                "records_found",
                "Unknown"
            )

            answer = response.get(
                "answer",
                "No response generated."
            )

            masked = response.get(
                "sensitive_data_masked",
                True
            )

            print_response(
                question=question,
                tool_used=tool_used,
                records_found=records_found,
                answer=answer,
                masked=masked
            )

            # Save output
            with open(
                "outputs/sample_prebuilt_agent_run.txt",
                "a",
                encoding="utf-8"
            ) as f:

                f.write(f"\nQuestion:\n{question}\n")
                f.write(f"\nTool Used:\n{tool_used}\n")
                f.write(f"\nRecords Found:\n{records_found}\n")
                f.write(f"\nAnswer:\n{answer}\n")
                f.write(f"\nSensitive Data Masked:\n{masked}\n")
                f.write("\n" + "=" * 80 + "\n")

        except Exception as e:

            print_response(
                question=question,
                tool_used="N/A",
                records_found=0,
                answer=f"Error: {str(e)}",
                masked=False
            )


if __name__ == "__main__":
    main()