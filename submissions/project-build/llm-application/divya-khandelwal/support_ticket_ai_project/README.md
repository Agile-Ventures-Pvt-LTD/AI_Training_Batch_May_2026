# Support Ticket AI Project
This project demonstrates how to use the GROQ API to analyze support tickets based on user-provided input. The application takes a structured ticket request, sends it to the GROQ model for analysis, and saves the response in a JSON file.

## Project Structure
- `app.py`: The main application file that orchestrates the workflow.
- `groq_client.py`: Contains the function to call the GROQ API.
- `validators.py`: Contains functions to validate the GROQ API key and the blog request.
- `prompts.py`: Contains the system and user messages used for the GROQ API call.
- `output_parser.py`: Contains functions to parse the GROQ response and store it in a JSON file.

## Expected Output
- The application will validate the GROQ API key and the blog request.
- If validation passes, the application will call the GROQ API with the provided messages.
- The response from the GROQ model will be parsed and saved in a JSON file within the `outputs` folder. The expected structure of the JSON.
This JSON file will contain the analysis of the blog intent based on the input provided, along with a summary of the input and any important points, missing information, and possible risks identified by the GROQ model.

