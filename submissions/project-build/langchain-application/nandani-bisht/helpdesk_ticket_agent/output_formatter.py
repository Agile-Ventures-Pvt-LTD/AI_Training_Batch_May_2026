def format_response(
    response,
    tools=None
):
    """
    Standard output formatting.
    """

    if tools is None:
        tools = []

    output = []

    output.append(
        "\nFINAL RESPONSE\n"
    )

    output.append(
        str(response)
    )

    if tools:

        output.append(
            "\nTOOLS USED"
        )

        for tool in tools:

            output.append(
                f"- {tool}"
            )

    return "\n".join(
        output
    )


def format_error(
    error
):
    """
    Error formatter.
    """

    return (
        "\nERROR\n"
        +
        str(error)
    )