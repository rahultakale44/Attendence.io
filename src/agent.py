"""
LangGraph agent implementation for attendance eligibility checking.
"""

from typing import Annotated
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from src.tools import check_attendance_eligibility, classes_needed_for_eligibility


def create_attendance_agent(with_memory=False):
    """
    Create a LangGraph attendance agent with tool calling capabilities.
    
    Args:
        with_memory: If True, compiles with InMemorySaver checkpointer for conversation memory
    
    Graph structure:
        START -> agent -> tools_condition -> tools -> agent -> END
    
    Returns:
        Compiled LangGraph application
    """
    # Initialize the model
    model = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )
    
    # Bind tools to the model
    tools = [check_attendance_eligibility, classes_needed_for_eligibility]
    model_with_tools = model.bind_tools(tools)
    
    # Define the agent node
    def agent_node(state: MessagesState):
        """Agent node that calls the LLM."""
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    # Create the graph
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    
    # Compile the graph with or without memory
    if with_memory:
        checkpointer = InMemorySaver()
        graph = builder.compile(checkpointer=checkpointer)
    else:
        graph = builder.compile()
    
    return graph
