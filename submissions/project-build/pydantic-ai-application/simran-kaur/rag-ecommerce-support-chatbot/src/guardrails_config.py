

from guardrails import Guard

from guardrails.hub import ProfanityFree



def input_guardrail(user_input: str):

    try:
        guard = Guard()

        guard.use(ProfanityFree(on_fail="filter"))
        guard.use(ToxicLanguage( threshold=0.5, validation_method="sentence", on_fail="filter"))

        validated = guard.validate(user_input)

        return validated.validated_output

    except Exception as e:

        raise ValueError(
            f"Input Guardrail Failed : {e}"
        )
    

def output_guardrail(user_input: str):

    try:
        guard = Guard()

        guard.use(ProfanityFree(on_fail="fix"))
        guard.use(ToxicLanguage( threshold=0.5, validation_method="sentence", on_fail="fix"))

        validated = guard.validate(user_input)

        return validated.validated_output

    except Exception as e:

        raise ValueError(
            f"Output Guardrail Failed : {e}"
        )
    

    