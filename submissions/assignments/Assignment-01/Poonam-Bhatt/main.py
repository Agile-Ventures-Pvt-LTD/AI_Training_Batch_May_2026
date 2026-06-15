from groq_client import generate_response
from prompts import FEW_SHOT_1
from utils import save_output, parse_json


result = generate_response(
    FEW_SHOT_1
)

print("\nMODEL OUTPUT:\n")

print(result)


parsed_result = parse_json(result)


if parsed_result:

    save_output(
        "outputs/FEW_SHOT_1_output.json",
        result
    )

    print("\nJSON Parsing Successful")

else:

    print("\nParsing failed.")