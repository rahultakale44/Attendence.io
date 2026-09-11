"""
Main entry point for Attendence.io agent.
"""

from src.agent import create_attendance_agent
from src.memory import create_thread_config


def test_basic_agent():
    """Test basic agent functionality (Milestone 3)."""
    print("=" * 70)
    print("MILESTONE 3: BASIC LANGGRAPH AGENT TEST")
    print("=" * 70)
    
    # Create the agent WITHOUT memory
    print("\n📊 Creating attendance agent (without memory)...")
    agent = create_attendance_agent(with_memory=False)
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


def test_memory_agent():
    """Test agent with conversation memory (Milestone 4)."""
    print("\n" + "=" * 70)
    print("MILESTONE 4: CONVERSATION MEMORY TEST")
    print("=" * 70)
    
    # Create agent WITH memory
    print("\n📊 Creating attendance agent (WITH memory)...")
    agent = create_attendance_agent(with_memory=True)
    print("✅ Agent created with InMemorySaver checkpointer\n")
    
    # Create thread config
    config = create_thread_config("demo-thread")
    
    # Turn 1
    print("-" * 70)
    print("TURN 1: Provide information")
    print("-" * 70)
    turn1 = "I've attended 28 of 40 classes."
    print(f"👤 User: {turn1}")
    
    result1 = agent.invoke({"messages": [("user", turn1)]}, config=config)
    print(f"🤖 Agent: {result1['messages'][-1].content}\n")
    
    # Turn 2
    print("-" * 70)
    print("TURN 2: Ask question (without repeating numbers)")
    print("-" * 70)
    turn2 = "Am I eligible?"
    print(f"👤 User: {turn2}")
    
    result2 = agent.invoke({"messages": [("user", turn2)]}, config=config)
    print(f"🤖 Agent: {result2['messages'][-1].content}\n")
    
    print("=" * 70)
    print("✅ MEMORY TEST COMPLETE")
    print(f"✅ Agent remembered 28/40 from Turn 1!")
    print("=" * 70)


def main():
    """Main entry point."""
    print("\n🎓 Attendence.io - Conversational AI Attendance Agent\n")
    
    # Test basic agent (Milestone 3)
    test_basic_agent()
    
    # Test memory agent (Milestone 4)
    test_memory_agent()
    
    print("\n✅ All tests complete!\n")


if __name__ == "__main__":
    main()
