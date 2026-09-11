"""
Tool call tracing utilities for debugging and verification.
"""


def print_trace(result: dict, title: str = "AGENT TRACE"):
    """
    Print detailed trace of agent execution including all tool calls.
    
    Args:
        result: The result dictionary from agent.invoke()
        title: Optional title for the trace output
    """
    print("\n" + "=" * 80)
    print(f"🔍 {title}")
    print("=" * 80)
    
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        
        print(f"\n[{i}] {msg_type}")
        print("-" * 80)
        
        # Human messages
        if msg_type == "HumanMessage":
            print(f"👤 User Input:")
            print(f"   {msg.content}")
        
        # AI messages
        elif msg_type == "AIMessage":
            # Check for tool calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"🤖 AI -> Calls Tool:")
                for tc in msg.tool_calls:
                    tool_name = tc['name']
                    tool_args = tc['args']
                    print(f"\n   Tool: {tool_name}")
                    print(f"   Arguments:")
                    for key, value in tool_args.items():
                        print(f"      {key}: {value}")
            else:
                # Final response
                print(f"🤖 AI Response:")
                content_lines = msg.content.split('\n')
                for line in content_lines:
                    print(f"   {line}")
        
        # Tool messages
        elif msg_type == "ToolMessage":
            if hasattr(msg, 'name'):
                print(f"🔧 Tool Result ({msg.name}):")
            else:
                print(f"🔧 Tool Result:")
            print(f"   {msg.content}")
    
    print("\n" + "=" * 80)


def print_tool_calls_only(result: dict):
    """
    Print only the tool calls from an agent execution.
    
    Args:
        result: The result dictionary from agent.invoke()
    """
    print("\n🔧 TOOL CALLS:")
    print("-" * 80)
    
    found_tool_calls = False
    
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            found_tool_calls = True
            for tc in msg.tool_calls:
                tool_name = tc['name']
                tool_args = tc['args']
                
                # Format as function call
                args_str = ", ".join([f"{k}={v}" for k, v in tool_args.items()])
                print(f"   {tool_name}({args_str})")
    
    if not found_tool_calls:
        print("   No tool calls found")
    
    print("-" * 80)


def print_compact_trace(result: dict):
    """
    Print a compact trace showing only key information.
    
    Args:
        result: The result dictionary from agent.invoke()
    """
    print("\n📊 COMPACT TRACE:")
    print("-" * 80)
    
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        
        if msg_type == "HumanMessage":
            content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
            print(f"[{i}] 👤 User: {content_preview}")
        
        elif msg_type == "AIMessage":
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    args_str = ", ".join([f"{k}={v}" for k, v in tc['args'].items()])
                    print(f"[{i}] 🤖 AI -> 🔧 {tc['name']}({args_str})")
            else:
                content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
                print(f"[{i}] 🤖 AI: {content_preview}")
        
        elif msg_type == "ToolMessage":
            content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
            print(f"[{i}] 🔧 Tool: {content_preview}")
    
    print("-" * 80)
