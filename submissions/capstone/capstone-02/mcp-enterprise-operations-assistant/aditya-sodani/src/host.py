import os
import json
import asyncio
from src.config import *
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from src.prompts import SYSTEM_PROMPT
from src.output_writer import save_query_result
from src.mcp_logger import reset_log,get_log
load_dotenv()



async def main():

    print("Enterprise Operations Assistant")

    client = MCPClient(MCP_CONFIG)


    llm = ChatGroq(
        model=GROQ_MODEL,
        temperature=0
    )

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=SYSTEM_PROMPT
    )

    while True:


        query=input("\nEnter Question: ")

        if query.lower()=="exit":
            break

        reset_log()

        result = await agent.run(query)

        print(
            "\nANSWER:\n",
            result
        )

        execution = get_log()

        save_query_result(
            user_query=query,
            servers_used=execution["servers_used"],
            tools_used=execution["tools_used"],
            evidence=execution["evidence"],
            operations_summary=str(result)
        )

        print("\nSaved to outputs/mandatory_query_results.json")


    await client.close_all_sessions()


if __name__=="__main__":
    asyncio.run(main())
 