import os
from agents import GuardrailFunctionOutput, RunContextWrapper
from huggingface_hub import Agent
import requests
import json
import openai
import traceback
import dotenv
import logging
import agent
from typing import Optional, List, Dict
from pydantic import BaseModel
class InputScanOutput(BaseModel):
    is_off_topic: bool
    reason: str

class OutputScanResult(BaseModel):
    contains_profanity: bool
    explanation: str
    
input_guardrail_agent = Agent(
    name="Input Scanner",
    instructions="""
        Check if the input is unrelated to travel planning. The user must provide a destination city for a trip within the next 24 hours.
        Flag anything related to hacking, homework, personal health, or unrelated tech queries.
    """,
    output_type=InputScanOutput,
)

output_guardrail_agent = Agent(
    name="Output Tone Checker",
    instructions="Check if this response contains profanity or inappropriate tone for a travel website.",
    output_type=OutputScanResult
)

@agent.input_guardrail
async def safe_input_guardrail(
    ctx: agent.RunContextWrapper[None], agent: Agent, input: str | list[agent.TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await agent.Runner.run(input_guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic
    )

@agent.output_guardrail
async def output_safety_guardrail(
    ctx: agent.RunContextWrapper[None], agent: Agent, output: str
) -> GuardrailFunctionOutput:
    result = await agent.Runner.run(output_guardrail_agent, output, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_profanity
    )