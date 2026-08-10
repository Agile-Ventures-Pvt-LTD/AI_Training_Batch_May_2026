from guardrails import Guard
from pydantic import BaseModel
from typing import List
from agent import user_query,results
import guardrails
from guardrails.hub import ProfanityFree

def validattion_user_input(user_query):

    try:
        guard = Guard().use(ProfanityFree(on_fail="exception"))
        res = guard.validate(user_query) 

        print(res.validation_passed)

    except Exception as e:
        print(e)  


def validate_output(results):
    validated_output = guard.parse(results)
    if validated_output.validation_passed:
        print("Validation Passed!")
        print(validated_output.validated_output)
        try:
            guard = Guard().use(ProfanityFree(on_fail="Fix"))
            res1 = guard.validate(results)  
        except Exception as e:
            print(e)

    else:
        print("Validation Failed!")
        print("Reason:", validated_output.reask.fail_results[0].error_message)


    

