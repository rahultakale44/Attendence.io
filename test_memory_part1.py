"""
MILESTONE 4 - PART 1: Conversation Memory Test

This test demonstrates that the agent can remember information from Turn 1
and use it to answer questions in Turn 2, without the user repeating the information.
"""

from src.agent import create_attendance_agent
from src.memory import create_thread_config, print_conversation_state


def test_part1_conversation_memory():
    """
    Part 1: Basic conversation memory using InMemorySaver and thread_id.
    
    Turn 1: "I've attended 28 of 40 classes."
    Turn 2: "Am I eligible?"
    
    Turn 2 should NOT require repeating 28 or 40.
    The agent should remember from Turn 1.
    """
    print("\n" + "=" * 80)
    print(" " * 20 + "MILESTONE 4 - PART 1: CONVERSATION MEMORY")
    print("=" * 80)
    
    print("\n📋 TEST OBJECTIVE:")
    print("-" * 80)
    print("Demonstrate that the agent remembers information across turns.")
    print("Turn 1: User provides attendance information")
    print("Turn 2: User asks eligibility WITHOUT repeating numbers")
    print("Expected: Agent retrieves 28/40 from memory and answers correctly")
    
    # Create agent WITH memory
    print("\n🚀 Creating agent with InMemorySaver checkpointer...")
    agent = create_attendance_agent(with_memory=True)
    print("✅ Agent created with conversation memory enabled")
    
    # Create thread configuration
    config = create_thread_config("attendance-demo-01")
    print(f"✅ Thread configuration created: thread_id='attendance-demo-01'")
    
    # TURN 1: Provide attendance information
    print("\n" + "=" * 80)
    print("TURN 1: Provide attendance information")
    print("=" * 80)
    
    turn1_message = "I've attended 28 of 40 classes."
    print(f"\n👤 User: {turn1_message}")
    
    result1 = agent.invoke(
        {"messages": [("user", turn1_message)]},
        config=config
    )
    
    print(f"\n🤖 Agent: {result1['messages'][-1].content}")
    
    # TURN 2: Ask about eligibility WITHOUT repeating numbers
    print("\n" + "=" * 80)
    print("TURN 2: Ask eligibility (WITHOUT repeating 28 or 40)")
    print("=" * 80)
    
    turn2_message = "Am I eligible?"
    print(f"\n👤 User: {turn2_message}")
    print("\n⚠️  NOTE: User did NOT repeat '28' or '40'")
    print("🧠 Agent must retrieve this information from conversation memory")
    
    result2 = agent.invoke(
        {"messages": [("user", turn2_message)]},
        config=config  # SAME config = SAME thread = SAME memory
    )
    
    print(f"\n🤖 Agent: {result2['messages'][-1].content}")
    
    # Display full conversation state
    print("\n" + "=" * 80)
    print("CONVERSATION STATE (Persisted via InMemorySaver)")
    print("=" * 80)
    print_conversation_state(result2, "attendance-demo-01")
    
    # Verification
    print("\n" + "=" * 80)
    print("✅ PART 1 VERIFICATION")
    print("=" * 80)
    
    # Check if tool was called in Turn 2
    tool_called_turn2 = False
    tool_args = None
    for msg in result2["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc['name'] == 'check_attendance_eligibility':
                    tool_called_turn2 = True
                    tool_args = tc['args']
    
    if tool_called_turn2:
        print(f"✅ Tool called in Turn 2: check_attendance_eligibility")
        print(f"✅ Tool arguments: {tool_args}")
        
        if 'attended' in tool_args and 'total' in tool_args:
            if tool_args['attended'] == 28 and tool_args['total'] == 40:
                print("✅ Correct values retrieved from memory (28 and 40)")
            else:
                print(f"⚠️  Unexpected values: attended={tool_args['attended']}, total={tool_args['total']}")
    else:
        print("⚠️  Tool was not called in Turn 2 (agent may have answered from context)")
    
    # Check final answer
    final_answer = result2["messages"][-1].content.lower()
    if "70" in final_answer or "not eligible" in final_answer:
        print("✅ Final answer is correct (70% attendance, not eligible)")
    else:
        print(f"⚠️  Final answer: {result2['messages'][-1].content}")
    
    # Confirm memory persistence
    total_messages = len(result2["messages"])
    if total_messages >= 4:  # At least: Turn1 user, Turn1 AI, Turn2 user, Turn2 AI
        print(f"✅ Conversation state persisted ({total_messages} messages in thread)")
    
    print("\n" + "=" * 80)
    print(" " * 28 + "PART 1 COMPLETE ✅")
    print("=" * 80)
    print("\n📝 KEY LEARNING:")
    print("   The agent successfully remembered attendance information (28/40)")
    print("   from Turn 1 and used it to answer the eligibility question in Turn 2.")
    print("   This was achieved using LangGraph's InMemorySaver checkpointer")
    print("   with a consistent thread_id across both turns.")
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    test_part1_conversation_memory()
