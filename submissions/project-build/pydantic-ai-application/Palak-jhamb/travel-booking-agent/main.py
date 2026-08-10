from src.agent import run_pipeline

def main():
    query=input("Enter your query: ")
    response=run_pipeline(query)
    print (response)


if __name__ == "__main__":
    main()
