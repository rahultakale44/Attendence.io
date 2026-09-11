"""
Conversation memory utilities for the attendance agent.
"""

from langgraph.checkpoint.memory import InMemorySaver


def create_thread_config(thread_id: str) -> dict:
    """
    Create a configuration dictionary for a specific conversation thread.
    
    Args:
        thread_id: Unique identifier for the conversation thread
        
    Returns:
        Configuration dict with thread_id for checkpointer
    """
    return {"configurable": {"thread_id": thread_id}}


def print_conversation_state(result: dict, thread_id: str = None):
    """
    Print the conversation state in a readable format.
    
    Args:
        result: The result from agent.invoke()
        thread_id: Optional thread ID to display
    """
    if thread_id:
        print(f"\n🧵 Thread ID: {thread_id}")
    
    print(f"📊 Total messages in conversation: {len(result['messages'])}")
    print("\n💬 Conversation history:")
    print("-" * 70)
    
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        
        if msg_type == "HumanMessage":
            print(f"\n[{i}] 👤 User: {msg.content}")
        elif msg_type == "AIMessage":
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"\n[{i}] 🤖 Agent: [Calling tool...]")
            else:
                content_preview = msg.content[:150] + "..." if len(msg.content) > 150 else msg.content
                print(f"\n[{i}] 🤖 Agent: {content_preview}")
        elif msg_type == "ToolMessage":
            print(f"[{i}] 🔧 Tool Result: {msg.content}")
    
    print("\n" + "-" * 70)
