import os
import re
import json
from typing import Dict,Any
from pathlib import Path
import asyncio
import sys
from langchain_groq import ChatGroq
from mcp_use import MCPClient,MCPServer,MCPAgent
from src.config import MCP_SERVER_CONFIG,GROQ_API_KEY,GROQ_MODEL,DATA_DIR
from src.prompts import System_Prompt
from src.tool_discovery import generate_mcp_schema_snapshot
from src.output_writer import write_mandatory_results,write_sample_runs

class Hostrun:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not defined in environment variable.")
        self.llm = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY,temperature=0)
        self.client = MCPClient(MCP_SERVER_CONFIG)
        self.agent = MCPAgent(llm=self.llm,client=self.client,max_steps=10,system_prompt=System_Prompt)
    
    async def query_processing(self,query:str)-> Dict[str,Any]:
        try:
            response_text = await self.agent.run(query)
            return self.parse_response(response_text,query)
    
        except Exception as e:
            return {
                'user_query':query,
                'error':str(e),
                'status':'fail'
            }
    
    def parse_response(self,response_text:str,original_query:str) -> Dict[str,Any]:
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {
                'user_query':response_text,
                'operation_summary':response_text,
                'servers_used':[],
                'tool_used':[],
                'status':'PASS'
            }
        summary_content = response_data.get('operation_summary')
        if isinstance(summary_content, str) and "```json" in summary_content:
            try:
                match = re.search(r"```json\s*(.*?)\s*```", summary_content, re.DOTALL)
                if match:
                    inner_json_str = match.group(1)
                    inner_data = json.loads(inner_json_str)
                    
                    if isinstance(inner_data, dict):
                        response_data.update(inner_data)
            except Exception:
                pass
        if "user_query" not in response_data or not  response_data['user_query']:
            response_data['user_query']= original_query
        response_data['tools_used'] = 'PASS'
        if 'tool_used' in response_data and 'tool_used' not in 'reponse_data':
            response_data['tool_used'] = response_data.pop('tool_used')
        return response_data
    
    async def close(self):
        await self.client.close_all_sessions()
    
async def run_server():
        host = Hostrun()
        print("Enterprise Operations Assistant")
        print("Connected MCP Servers:")
        for name in MCP_SERVER_CONFIG['mcpServers'].keys():
            print(f"-{name}")
        print("\n Enter your question (or 'exit' for quit):")
        while True:
            query = input(">")
            if query.lower()=='exit':
                break
            print('Processing.....')
            result = await host.query_processing(query)
            print("\nResult:")
            print(json.dumps(result,indent=2))

            write_mandatory_results([result])
            write_sample_runs([result])
            print('\n')
        await host.close()

async def manadatory_queries():
        host =Hostrun()
        await generate_mcp_schema_snapshot()
        with open (DATA_DIR/"sample_queries.json",'r') as f:
            data = json.loads(f)
        if isinstance(data,dict) and 'mandatory_queries' in data:
            queries = data['mandatory_queries']
        elif isinstance(data,list):
            queries =data
        else:
            queries=[]
        results = []
        for q in queries:
            if not isinstance(q,dict):
                continue
            query_text = q.get('query','')
            query_id = q.get('id',"Query")
            if not query_text.strip():
                continue
            print(f'processing {query_id}:{query_text}')
            result = await host.query_processing(query_text)
            result['query_id'] = query_id
            results.append(result)

        write_mandatory_results(results)
        write_sample_runs(results)
        await host.close()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--run-mandatory":
        asyncio.run(manadatory_queries())
    else:
        asyncio.run(run_server())


            

        

    


        

# async def init_and_query_agent(user_query:str)-> str:
#     if not GROQ_API_KEY:
#         raise ValueError("GROQ_API_KEY is not defined in environment variable.")
    
#     llm = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY,temperature=0)

#     client = MCPClient(MCP_SERVER_CONFIG)
#     agent = MCPAgent(llm=llm,client=client,max_steps=10,system_prompt=System_Prompt)
#     response = await agent.run(user_query)
#     await client.close()
#     return response

# def start_session()-> None:
#     print("Enterprise Operations Assistant")
#     print("Connected MCP Servers:")
#     print("- service-health")
#     print("- support-ticket")
#     print("- change-management")

#     if len(sys.argv)>1:
#         query = " ".join(sys.argv[1:])
#         print(f"\n Enter your Question: > {query}")
#         print('processing')
#         output = asyncio.run(init_and_query_agent(query))
#         print(output)
#     else:
#         while True:
#             try:
#                 query =input("\n Enter your question: >")
#                 if not query.strip():
#                     continue
#                 print('processing')
#                 output= asyncio.run(init_and_query_agent(query))
#             except(KeyboardInterrupt,EOFError):
#                 print("\n Session Stop")
#                 break

# if __name__ == '__main__':
#     start_session()

# # import os
# # import asyncio
# # import sys
# # from langchain_groq import ChatGroq
# # from mcp_use import MCPClient, MCPServer, MCPAgent 
# # from src.config import MCP_SERVER_CONFIG, GROQ_API_KEY, GROQ_MODEL
# # from src.prompts import System_Prompt

# # async def run_agent_query(agent: MCPAgent, user_query: str) -> str:
# #     print('Processing...')
# #     response = await agent.run(user_query)
# #     return response

# # async def main_async_loop():
# #     llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
# #     client = MCPClient(MCP_SERVER_CONFIG)
# #     agent = MCPAgent(llm=llm, client=client, max_steps=10, system_prompt=System_Prompt)
    
# #     try:
# #         if len(sys.argv) > 1:
# #             query = " ".join(sys.argv[1:])
# #             print(f"\nEnter your Question: > {query}")
# #             output = await run_agent_query(agent, query)
# #             print(output)
# #         else:
# #             while True:
# #                 try:
# #                     query = input("\nEnter your question: > ")
# #                     if not query.strip():
# #                         continue
# #                     output = await run_agent_query(agent, query)
# #                     print(output)
# #                 except (KeyboardInterrupt, EOFError):
# #                     print("\nSession Stop")
# #                     break
# #     finally:
# #         print("Closing MCP Server connections...")
# #         await client.close()

# # def start_session() -> None:
# #     print("Enterprise Operations Assistant")
# #     print("Connected MCP Servers:")
# #     print("- service-health")
# #     print("- support-ticket")
# #     print("- change-management")
    
# #     if not GROQ_API_KEY:
# #         print("Error: GROQ_API_KEY is not defined in environment variables.", file=sys.stderr)
# #         sys.exit(1)
        
# #     asyncio.run(main_async_loop())

# # if __name__ == '__main__':
# #     start_session()
