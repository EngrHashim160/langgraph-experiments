from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    

model = ChatOpenAI(temperature=0)

def make_default_graph():
    workflow = StateGraph(State)
    
    def call_model(state: State):
        return {
            'messages': [model.invoke(state['messages'])]
        }
    
    workflow.add_node('agent', call_model)
    workflow.add_edge('agent', START)
    workflow.add_edge('agent', END)
    
    agent = workflow.compile()
    
    return agent

agent = make_default_graph()


