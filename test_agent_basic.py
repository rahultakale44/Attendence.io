"""
Detailed test of basic agent functionality with tool call verification.
"""

from src.agent import create_attendance_agent


def test_agent_with_tool_verification():
    """Test agent and verify tool calls are happening."""
    print("\n" + "=" * 70)
    print("DETAILED AGENT TEST WITH TOOL CALL VERIFICATION")
    print("=" * 70)
    
    # Create agent
    agent = create_attendance_agent()
    
    # Test question
    question = "I attended 28 out of 40 classes. Am I eligible?"
    print(f"\n❓ Question: {question}\n")
    
    # Invoke agent
    result = agent.invoke({"messages": [("user", question)]})
    
    # Analyze the messages
    print("📊 MESSAGE FLOW:")
    print("-" * 70)
    
    for i, msg in enumerate(result["messages"]):
        msg_type = type(msg).__name__
        print(f"\n[{i}] {msg_type}")
        
        if hasattr(msg, 'content') and msg.content:
            content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            print(f"    Content: {content_preview}")
        
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"    🔧 Tool Calls: {len(msg.tool_calls)}")
            for tc in msg.tool_calls:
                print(f"       - Tool: {tc['name']}")
                print(f"       - Args: {tc['args']}")
        
        if hasattr(msg, 'name') and msg.name:
            print(f"    Tool: {msg.name}")
    
    # Final answer
    print("\n" + "=" * 70)
    print("📋 FINAL ANSWER:")
    print("=" * 70)
    final_message = result["messages"][-1]
    print(f"\n{final_message.content}\n")
    
    # Verification
    print("=" * 70)
    print("✅ VERIFICATION:")
    print("=" * 70)
    
    # Check if tool was called
    tool_called = False
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            tool_called = True
            break
    
    if tool_called:
        print("✅ Tool was called by the LLM")
    else:
        print("❌ Tool was NOT called by the LLM")
    
    # Check if answer contains expected information
    final_content = final_message.content.lower()
    if "70" in final_content or "not eligible" in final_content or "below" in final_content:
        print("✅ Answer contains correct attendance information")
    else:
        print("⚠️  Answer may not contain expected information")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    test_agent_with_tool_verification()
