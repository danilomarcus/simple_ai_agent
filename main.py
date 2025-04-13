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
    print("Iniciando a criação do LLM OpenAI...")
    llm_openai = ChatOpenAI(model="gpt-4o-mini")
    print(f"LLM OpenAI criado: {llm_openai}")
    
    print("Criando o parser...")
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    print(f"Parser criado: {parser}")
    
    print("Criando o prompt...")
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
    print(f"Prompt criado: {prompt}")
    
    print("Adicionando instruções de formatação ao prompt...")
    format_instructions = parser.get_format_instructions()
    print(f"Instruções de formatação: {format_instructions}")
    
    prompt_with_format = prompt.partial(format_instructions=format_instructions)
    print(f"Prompt com instruções de formatação: {prompt_with_format}")
    
    print("Criando o agente...")
    tools = [search_tool, wikipedia_tool, save_to_txt_tool]
    agent = create_tool_calling_agent(
        llm=llm_openai,
        prompt=prompt_with_format,
        tools=tools
    )
    print(f"Agente criado: {agent}")
    
    print("Criando o executor do agente...")
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    print(f"Executor do agente criado: {agent_executor}")
    
    print("Invocando o agente executor...")
    query = input("How can I help you today? ")
    raw_response = agent_executor.invoke({"query": query})

    structured_response = parser.parse(raw_response.get("output"))
    print(f"Resposta estruturada: {structured_response}")
    
except Exception as e:
    print(f"Erro detectado: {str(e)}")
    print("Traceback completo:")
    traceback.print_exc()