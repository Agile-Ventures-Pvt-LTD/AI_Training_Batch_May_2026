import sys
import os
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from tools import inspect_database_schema, get_customer_profile, get_card_details, search_transactions, get_customer_transactions, get_statement_summary, get_rewards_summary, get_merchant_spend_summary
import json

result = inspect_database_schema.invoke({})

print(result)

result = get_customer_profile.invoke(
    {
        "cust_id": "1"
    }
)

print(result)


with open(
    "tool_outputs/customer_profile_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )


result = get_card_details.invoke(
    {
        "cust_id": "1"
    }
)

print(result)

os.makedirs(
    "tool_outputs",
    exist_ok=True
)

with open(
    "tool_outputs/card_details_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

result = search_transactions.invoke(
    {
        "customer_id": "1",
        "limit": 5
    }
)

print(result)


with open(
    "tool_outputs/search_transactions_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )



result = get_customer_transactions.invoke(
    {
        "customer_id": "1",
        "limit": 5
    }
)

print(result)

with open(
    "tool_outputs/customer_transactions_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

result = get_statement_summary.invoke(
    {
        "customer_id": "1"
    }
)

print(result)


with open(
    "tool_outputs/statement_summary_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

import json
import os

result = get_rewards_summary.invoke(
    {
        "customer_id": "1"
    }
)

print(result)

os.makedirs(
    "tool_outputs",
    exist_ok=True
)

with open(
    "tool_outputs/rewards_summary_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

result = get_merchant_spend_summary.invoke(
    {
        "customer_id": "1",
        "group_by": "merchant_type"
    }
)

print(result)


with open(
    "tool_outputs/merchant_spend_summary_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )


from tools import detect_suspicious_transactions
import json
import os

result = detect_suspicious_transactions.invoke(
    {
        "customer_id": "1"
    }
)

print(result)


with open(
    "tool_outputs/suspicious_transactions_output.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )