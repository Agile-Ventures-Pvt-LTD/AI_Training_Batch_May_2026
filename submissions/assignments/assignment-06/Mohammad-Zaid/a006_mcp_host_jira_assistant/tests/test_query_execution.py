from src.prompts import SYSTEM_PROMPT

def test_prompt_exists():

    assert SYSTEM_PROMPT is not None
    assert len(SYSTEM_PROMPT) > 0