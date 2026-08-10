
#===============================LEGACY AGENT TESTS===============================
from src.agents.legacy_agent import (
    run_agent
)


def test_customer_count():

    response = run_agent(
        "How many customers exist?"
    )

    assert len(response) > 0
    print("\nLegacy Agent Response:\n")
    print(response)


#===============================MODERN AGENT TESTS===============================

# from src.agents.modern_agent import (
#     run_agent
# )


# def test_order_count():

#     response = run_agent(
#         "How many orders exist?"
#     )

#     assert len(response) > 0
#     print("\nModern Agent Response:\n")
#     print(response)


#============================================================================================================
# # run ```pytest tests/test_agent_queries.py``` to execute
# run ```pytest tests/test_agent_queries.py -v -s``` to execute with verbose output and print statements
#============================================================================================================