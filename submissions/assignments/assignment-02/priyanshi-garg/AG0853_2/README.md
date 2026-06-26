## Assignment 02 - Query Expansion

## Participant Name
Priyanshi Garg

## Description
This assignment focuses on improving retrieval performance using **query expansion**. The objective is to generate multiple variations of the user's original query and send each variation to the retriever. The retriever returns relevant chunks for every query version, after which a set operation is applied to remove duplicate chunks and obtain a unique collection of retrieved documents. These unique chunks are then provided as context to the LLM along with the system prompt and the user's query, enabling the model to generate more comprehensive and accurate responses.


## How to Run

```terminal
uv add -r requirements.txt
Run each cell of 2_RAG_TESLAReports_all-mpnet-base-v2.ipynb
````

## Files Included

* 2_RAG_TESLAReports_all-mpnet-base-v2.ipynb
* requirements.txt
* README.md

## Notes

The API key is not included in the code. Please set it using an environment variable.