"""
Main entry point for Attendence.io agent.
"""

from src.agent import create_attendance_agent


def test_basic_agent():
    """Test basic agent functionality with a simple attendance question."""
    print("=" * 70)
    print("MILESTONE 3: BASIC LANGGRAPH AGENT TEST")
    print("=" * 70)
    
    # Create the agent
    print("\n📊 Creating attendance agent...")
    agent = create_attendance_agent()
    print("✅ Agent created successfully\n")
    
    # Test question
    question = "I attended 28 out of 40 classes. Am I eligible?"
    print(f"❓ Question: {question}\n")
    
    # Invoke the agent
    print("🤖 Agent processing...\n")
    result = agent.invoke({"messages": [("user", question)]})
    
    # Display results
    print("-" * 70)
    print("📋 AGENT RESPONSE:")
    print("-" * 70)
    
    # Get the final message
    final_message = result["messages"][-1]
    print(f"\n{final_message.content}\n")
    
    print("=" * 70)
    print("✅ BASIC AGENT TEST COMPLETE")
    print("=" * 70)
    
    return result


def main():
    """Main entry point."""
    print("\n🎓 Attendence.io - Conversational AI Attendance Agent\n")
    
    # Run basic agent test
    test_basic_agent()


if __name__ == "__main__":
    main()
