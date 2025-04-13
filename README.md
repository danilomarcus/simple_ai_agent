# AI Research Assistant agent

A simple example on how to use a model to build your own agent using some tools

## Overview

This project creates an AI-powered research assistant that:

1. Takes user queries about research topics
2. Uses multiple tools (web search, Wikipedia [you may add more if needed]) to gather relevant information
3. Synthesizes the information into a structured research response
4. Provides sources and saves the output to a text file

## Components

### main.py

The main application file that:
- Sets up the LangChain agent with OpenAI integration [you can use Anthropic as well]
- Defines a Pydantic model for structured output
- Creates a research assistant agent with tool-calling capabilities
- Handles user input and processes responses

### tools.py

Defines the tools available to the research assistant:
- `search_tool`: Uses DuckDuckGo to search the web for information
- `wikipedia_tool`: Queries Wikipedia for relevant information
- `save_to_txt_tool`: Saves research outputs to a text file with timestamps

## Setup Instructions

### 1. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Running the Application

```bash
python main.py
```

When prompted, enter your research query, and the assistant will gather information and generate a structured response.

## Output

The research output includes:
- Topic of research
- Summary of findings
- Sources used
- Tools used in the research process

Results are displayed in the terminal and also saved to a `research_output.txt` file for future reference.

## Requirements

See `requirements.txt` for the complete list of dependencies, which includes:
- langchain
- wikipedia
- langchain-community
- langchain-openai
- langchain-anthropic
- python-dotenv
- pydantic
- duckduckgo-search

## Notes

- The application requires API keys for OpenAI and/or Anthropic to function
- By default, the application uses the "gpt-4o-mini" model, but you can modify this in the code
- Make sure you have sufficient quota available in your OpenAI account