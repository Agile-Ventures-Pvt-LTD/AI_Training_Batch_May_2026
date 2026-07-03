from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails.hub import ToxicLanguage



validation_check=Guard.use_many(
    ProfanityFree(on_fail="exception"),
    ToxicLanguage(on_fail="exception")
)

output="You are a good person"
res=validation_check.validate(output)
print(res.validate_passed)


