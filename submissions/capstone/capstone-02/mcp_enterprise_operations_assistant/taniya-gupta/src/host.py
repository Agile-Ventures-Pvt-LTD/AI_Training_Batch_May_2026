import os
import sys
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPClient, MCPAgent
import argparse


load_dotenv()

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.prompts import SYSTEM_PROMPT, STRUCTURE_PROMPT
from src.config import config
from src.tool_discovery import run_tool_discovery
from src.output_writer import (
    save_output_samples,
    save_query_result,
    parse_execution_history
)

async def structure_the_results(llm,query, nl_response, evidence):
    "Structuring the natural language response and evidence into json format"
    prompt= STRUCTURE_PROMPT.format(
        query=query,
        response=nl_response,
        evidence=json.dumps(evidence, indent=2)
    )
    try:
        res=await llm.invoke(prompt)
        content=res.content.strip() # cleaning the result
        structured=json.loads(content)
        return structured
    except Exception as e:
        return {
            "operations_summary" : nl_response,
            "possible_change_correlation" : "",
            "recommended_next_actions": [],
            "Limitations" : [f"{str(e)}"]}
    
async def run_query(llm, client, query):
    """Run a single query and return the response + parsed history metadata"""
    agent=MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=SYSTEM_PROMPT
    )
    response= await agent.run(query)
    history=agent.get_conversation_history()
    servers_used, tools_used , evidence= parse_execution_history(history)
    structured= await structure_the_results(llm, query, response, evidence)
    return response, servers_used, tools_used , evidence, structured

async def batch_run():
    """To run all mandatory queries"""
    load_dotenv()
    await run_tool_discovery()
    client=MCPClient(config)
    llm= ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    file= Path(__file__).resolve().parent.parent / "data" / "sample_queries.json"

    with open (file, "r") as f:
            data=json.load(f)
    queries=data.get("mandatory_queries")
    results=[]
    try:
        await client.create_all_sessions()
        for q in queries:
            qid=q.get("id")
            querytext=q.get("query")
            nl_response, servers_used, tools_used, evidence, structured= await run_query(llm, client, querytext)
            print(f"{nl_response}")
            result={
                "query_id" : qid,
                "user_query" : querytext,
                "servers_used" :servers_used,
                "tools_used" : tools_used,
                "evidence" : evidence,
                "operations_summary" : structured.get("operations_summary"),
                "possible_change_correlation" :structured.get("possible_change_correlation"),
                "recommended_next_actions": structured.get("recommended_next_actions"),
                "limitations": structured.get("limitations"),
                "final_answer": nl_response
            }
            results.append(result)
    finally:
        await client.close_all_sessions()
    save_query_result(results)
    save_output_samples(results)

async def run_project():
    load_dotenv()
    await run_tool_discovery()
    client=MCPClient(config)
    llm= ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    try:
        await client.create_all_sessions()
        while True:
            try:
                print("Capstone-02")
                print("To exit the loop, type 'exit' or 'quit'")
                question= input("Enter your query: ").strip()
                if not question:
                    continue
                if question in ["exit", "quit"]:
                    break
                response, _, _, _, _, = await run_query(llm, client, question)
                print(f"{response}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                return {"error" : str(e)}
    finally:
        await client.close_all_sessions()

def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true")
    args=parser.parse_args()

    if args.batch:
        asyncio.run(batch_run())
    else:
        asyncio.run(run_project())


if __name__=="__main__":
    main()