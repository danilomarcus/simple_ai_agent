from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
import traceback
from tools import search_tool, wikipedia_tool, save_to_txt_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

try:
    llm_openai = ChatOpenAI(model="gpt-4o-mini")
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper.
                Answer the user query and use neccessary tools. 
                Wrap the output in this format and provide no other text\n{format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    
    format_instructions = parser.get_format_instructions()
    prompt_with_format = prompt.partial(format_instructions=format_instructions)
    
    tools = [search_tool, wikipedia_tool, save_to_txt_tool]
    agent = create_tool_calling_agent(
        llm=llm_openai,
        prompt=prompt_with_format,
        tools=tools
    )
    
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    
    query = input("How can I help you today (q to quit)? ")
    if query == "q":
        print("Exiting...")
        exit()

    raw_response = agent_executor.invoke({"query": query})
    
    # Verificar se raw_response não é None antes de tentar usar .get()
    if raw_response is not None:
        output = raw_response.get("output", "")
        if output:
            try:
                structured_response = parser.parse(output)
                print(f"structured_response: {structured_response}")
            except Exception as parsing_error:
                print(f"Error parsing output: {str(parsing_error)}")
                print(f"Raw output: {output}")
        else:
            print("No output was returned from the agent.")
    else:
        print("Agent returned None response.")
    
except Exception as e:
    print(f"Error: {str(e)}")
    print("complete traceback:")
    traceback.print_exc()