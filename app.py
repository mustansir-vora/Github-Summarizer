import os
import re
import streamlit as st
from github import Github
from streamlit_agraph import agraph, Node, Edge, Config
from gemini import generate_ai_description_with_gemini
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
github = Github(GITHUB_TOKEN)

# Fetch repository files
def fetch_repo_files(repo_name):
    repo = github.get_repo(repo_name)
    contents = repo.get_contents("")
    files = []
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "file":
            files.append(file_content)
        elif file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
    
    return files, repo.description

# Extract code snippets from the files
def extract_code_snippets(files):
    code_snippets = []
    for file in files:
        if file.name.endswith((".py", ".js", ".java", ".jsx", ".json", ".c", ".go", ".ipynb")):  # Adjust extensions as needed
            content = file.decoded_content.decode("utf-8")
            code_snippets.append(content[:5000])  # Limit snippet size to avoid token overflow
    return code_snippets

def extract_code_data(files):
    """Extracts code and pairs it with the filename for better context."""
    code_data = []
    for file in files:
        if file.name.endswith((".py", ".js", ".java", ".jsx", ".json", ".c", ".go", ".ipynb")):
            content = file.decoded_content.decode("utf-8")
            code_data.append({
                "filename": file.name,
                "content": content[:5000] # Limit to avoid token overflow
            })
    return code_data

# Extract function names using regex (customize for different languages)
def extract_function_names(code):
    function_names = []
    
    # Regex patterns for various language functions
    patterns = [
        r"def (\w+)\(",  # Python function definition
        r"function (\w+)\(",  # JavaScript function definition
        r"public\s+[\w<>\[\]]+\s+(\w+)\(",  # Java function definition
        r"(\w+)\s*=\s*function\s*\(",  # JS anonymous function
        r"func (\w+)\(",  # Go function definition
        r"fun (\w+)\(",  # Kotlin function definition
        r"fun (\w+)\s*\(",  # Dart function definition
        r"^\s*def\s+(\w+)\s*\(",  # Python function definition (indented code in Jupyter)
        r"(\w+)\s*\(\)\s*{",  # JSX function definition (React function component)
        r"const\s+(\w+)\s*=\s*\(\)\s*=>\s*{",  # JSX arrow function definition (React)
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, code)
        function_names.extend(matches)
    
    return function_names

# Generate graph from code snippets
def generate_code_graph(code_snippets):
    nodes = []
    edges = []
    
    for snippet in code_snippets:
        function_names = extract_function_names(snippet)  # Extract function names
        
        for function in function_names:
            nodes.append(Node(id=function, label=function))  # Add each function as a node
        
        # Example logic to generate edges (if you have related functions, you can customize this)
        for i in range(len(function_names)-1):
            edges.append(Edge(source=function_names[i], target=function_names[i+1]))  # Create an edge between functions
    
    return nodes, edges

def generate_architectural_graph(code_data):
    """Generates a graph mapping Files -> Functions."""
    nodes = []
    edges = []
    added_nodes = set()
    
    for file_data in code_data:
        filename = file_data["filename"]
        functions = extract_function_names(file_data["content"])
        
        # Add File Node
        if filename not in added_nodes:
            nodes.append(Node(id=filename, label=filename, size=25, shape="hexagon", color="#FF4B4B"))
            added_nodes.add(filename)
            
        # Add Function Nodes and link them to the File
        for func in functions:
            func_id = f"{filename}_{func}" # Unique ID to prevent cross-file conflicts
            if func_id not in added_nodes:
                nodes.append(Node(id=func_id, label=func, size=15, shape="dot", color="#4B8BFF"))
                added_nodes.add(func_id)
                edges.append(Edge(source=filename, target=func_id, color="#FFFFFF"))
                
    return nodes, edges

# Function to fetch repo details and commit data
def fetch_repo_details(repo_name):
    repo = github.get_repo(repo_name)
    commits = repo.get_commits()
    description = repo.description
    commit_dates = [commit.commit.author.date for commit in commits]
    
    return {
        "name": repo_name,
        "description": description,
        "commit_count": commits.totalCount,
        "commit_dates": commit_dates,
        "ai_description": ai_description,  # Adding AI-generated description
        "code_snippets": code_snippets  # Including code snippets
    }

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("GitHub Repository Deep-Dive Summarizer")
repo_name = st.text_input("Enter the GitHub Repository (owner/repo):", placeholder="e.g., streamlit/streamlit")

if repo_name:
    with st.spinner("Analyzing repository architecture and executing deep dive..."):
        try:
            # 1. Fetch files and basic info
            files, description = fetch_repo_files(repo_name)
            
            # 2. Extract code paired with filenames
            code_data = extract_code_data(files)

            compiled_code = "\n".join([f"--- FILE: {d['filename']} ---\n{d['content']}\n" for d in code_data])
            
            # 3. Generate Architectural Graph
            nodes, edges = generate_architectural_graph(code_data)
            
            # Make sure your gemini.py function accepts this prompt string!
            ai_deep_dive = generate_ai_description_with_gemini(compiled_code) 
            
            # --- Rendering ---
            st.write(f"### Repository: {repo_name}")
            if description:
                st.write(f"_{description}_")
                
            st.markdown("---")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.write("### File Architecture Graph")
                st.caption("Red Hexagons = Files | Blue Dots = Functions extracted from that file")
                
                config = Config(
                    width="100%",
                    height=700,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    nodeHighlightBehavior=True,
                    highlightColor="#F7A7A6"
                )
                agraph(nodes=nodes, edges=edges, config=config)
                
            with col2:
                st.write("### Step-by-Step Execution & Analysis")
                st.write(ai_deep_dive)
            
            
            
        except Exception as e:
            st.error(f"Error fetching repository details: {e}")
