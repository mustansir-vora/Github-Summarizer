import google.generativeai as gemini
import os
from dotenv import load_dotenv
load_dotenv()

gemini.configure(api_key=os.getenv("GEMINI_KEY"))

def generate_ai_description_with_gemini(code_snippets):
    prompt = f"""
    You are a senior software architect. I am providing you with the source code of a GitHub repository. 
    
    Your task is to explain this project in great depth. Please structure your response with the following sections:
    
    1. **High-Level Overview**: What does this project do?
    2. **Step-by-Step Execution Flow**: Trace the logic of the application from the entry point (or main scripts) down to the core functionalities. Explain how the files and functions interact with one another.
    3. **Crucial Code Snippets**: Identify the most important blocks of code in this repository. Output these specific snippets and explain exactly what makes them the "engine" of the project.
    4. **Dependencies & Architecture**: Briefly summarize the architecture and tools used.
    
    Here is the repository code:
    {code_snippets}
    """
    model = gemini.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    
    return response.text



