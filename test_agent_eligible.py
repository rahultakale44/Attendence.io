"""
Test agent with an eligible student scenario.
"""

from src.agent import create_attendance_agent


def test_eligible_student():
    """Test agent with a student who is eligible."""
    print("\n" + "=" * 70)
    print("TEST: ELIGIBLE STUDENT")
    print("=" * 70)
    
    # Create agent
    agent = create_attendance_agent()
    
    # Test question - student with 36/40 (90%)
    question = "I attended 36 out of 40 classes. Am I eligible?"
    print(f"\n❓ Question: {question}\n")
    
    # Invoke agent
    result = agent.invoke({"messages": [("user", question)]})
    
    # Show tool call
    print("🔧 TOOL CALL:")
    print("-" * 70)
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"Tool: {tc['name']}")
                print(f"Args: {tc['args']}")
    
    # Show tool result
    print("\n📊 TOOL RESULT:")
    print("-" * 70)
    for msg in result["messages"]:
        if hasattr(msg, 'name') and msg.name == 'check_attendance_eligibility':
            print(msg.content)
    
    # Final answer
    print("\n📋 FINAL ANSWER:")
    print("-" * 70)
    final_message = result["messages"][-1]
    print(f"{final_message.content}\n")
    
    print("=" * 70)
    print("✅ TEST COMPLETE\n")


if __name__ == "__main__":
    test_eligible_student()
