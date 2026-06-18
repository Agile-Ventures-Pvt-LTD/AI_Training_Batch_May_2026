def print_response(
    question,
    tool_used,
    records_found,
    answer,
    masked
):

    print("\n" + "=" * 80)

    print("\nQuestion:")
    print(question)

    print("\nTool Used:")
    print(tool_used)

    print("\nRecords Found:")
    print(records_found)

    print("\nAnswer:")
    print(answer)

    print("\nSensitive Data Masked:")
    print(masked)

    print("\n" + "=" * 80)