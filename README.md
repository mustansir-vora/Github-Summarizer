
# GitHub Repository Deep-Dive Summarizer 🔖

## Overview

This tool analyzes and visualizes any public GitHub repository. It fetches the codebase, analyzes the architecture, visualizes file/function relationships, and generates AI-powered summaries and commit activity graphs.

---

## Features

- **AI-Powered Summaries:** Uses Gemini to generate detailed explanations of the repository's code and structure.
- **Architecture Visualization:** Interactive graph showing files (red hexagons) and their functions (blue dots) using Streamlit AGraph.
- **Commit Activity Graph:** Visualizes commit frequency over time with Plotly.
- **Simple UI:** Built with Streamlit for easy use and fast results.

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Github_repo_summarizer.git
   cd Github_repo_summarizer
   ```

2. **Install dependencies:**
   ```bash
   pip install streamlit PyGithub python-dotenv streamlit-agraph pandas plotly matplotlib
   ```

3. **API Keys Required:**
   - **GitHub Token:** (classic, with repo read access)
   - **Gemini API Key:** (for AI summaries)
   - Store these in a `.env` file:
     ```env
     GITHUB_TOKEN=your_github_token
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. Enter the repository name in the format `owner/repo` (e.g., `streamlit/streamlit`).
2. Wait for the analysis to complete. The UI will display:
   - File/function architecture graph
   - AI-generated deep-dive summary
   - Commit activity chart

---

## How it Works

- Fetches all files and commit history from the specified GitHub repo.
- Extracts code and function names from supported file types.
- Compiles the code for AI analysis and sends it to Gemini for a detailed summary.
- Visualizes the file/function structure and commit activity.

---

## Built With

- [Streamlit](https://streamlit.io/) — UI framework
- [PyGithub](https://pygithub.readthedocs.io/) — GitHub API access
- [streamlit-agraph](https://github.com/ChrisDelClea/streamlit-agraph) — Graph visualization
- Gemini (Google Generative AI) — AI code summarization
- [Plotly](https://plotly.com/python/) & [Matplotlib](https://matplotlib.org/) — Data visualization
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

---

## Example Input

```
streamlit/streamlit
```

---

## License

MIT License




