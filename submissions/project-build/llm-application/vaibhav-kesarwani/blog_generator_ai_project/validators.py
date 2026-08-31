def get_non_empty_string(prompt, error_message):
    """Validate required string inputs."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print(error_message)


def get_list_input(prompt, error_message, required=True):
    """
    Validate list inputs entered as comma-separated values.
    """
    while True:
        value = input(prompt).strip()

        if not value:
            if required:
                print(error_message)
                continue
            return []

        items = [item.strip() for item in value.split(",") if item.strip()]

        if items:
            return items

        print(error_message)