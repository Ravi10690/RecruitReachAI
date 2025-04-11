import os
from agents import Agent, Runner, WebSearchTool
from RecruitReach_AI.utils.toml_parser import TomlParser
tomlparser = TomlParser()
os .environ['OPENAI_API_KEY'] = tomlparser.get_value('openai', 'OPENAI_API_KEY')
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that search on web about a given company name and return the information",
    tools=[
        WebSearchTool(),
    ],
)

def get_company_info(company_name):
    mesages = Runner.run_sync(agent, company_name)
    return message.final_output