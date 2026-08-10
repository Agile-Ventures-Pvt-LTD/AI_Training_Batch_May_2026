# Step-01: Load environment variable
## .env.example

Loading multiple variables in .env.example:
GROQ_API_KEY
GROQ_MODEL
EMBEDDING_MODEL
VECTOR_DB
CHUNK_SIZE
CHUNK_OVERLAP
TOP_K

# Step-02: Loading the documents

Loading the documents using PyPDF Loader to load the pdf "Amazon-2025-Annual-Report.pdf"

# Step-03: Preprocessing the documents
## Chunking

Dividing the whole text into chunks using Batch-size of 1000.

## Generate embeddings

Converting the chunks into their corresponding numerical values using embedding function and embedding models.

## Storing the embeddings into vectorDB

After conversion into embeddings, those embeddings are being stored in a vectorDB i.e. ChromaDB in the current scenario.

## Accept user question

Taking user query as input.

## Classifying the query type

Whether the query is for only answering, generating summary or classification.

## Retrieving

Retrieving the top-K relevant chunks for giving output of the query.

## Build grounded RAG prompt

Building the prompt for RAG model according to the user query requirements.

## Generating the answer

Generating the answer using GROQ model.

## Save outputs to log

Saving the outputs for record.

## Run Benchmark questions

Running the benchmark questions for testing the model's accuracy and reliability.

# Author 

Vaishnavi Gupta