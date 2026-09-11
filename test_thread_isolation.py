"""
MILESTONE 6 - PART 2: Thread Isolation Test

This test demonstrates that different thread_ids maintain separate
conversation memories. Thread A's information is NOT accessible to Thread B.
"""

from src.agent import create_attendance_agent
from src.memory import create_thread_config
from src.trace import print_compact_trace, print_tool_calls_only


def test_thread_isolation():
    """
    Part 2: Thread isolation using different thread_id values.
    
    Thread A: Provides attendance info (28/40)
    Thread B: Asks "Am I eligible?" - should NOT know Thread A's data
    Thread A: Asks "Am I eligible?" - should still remember its own data
    """
    print("\n" + "=" * 80)
    print(" " * 20 + "MILESTONE 6 - PART 2: THREAD ISOLATION")
    print("=" * 80)
    
    print("\n📋 TEST OBJECTIVE:")
    print("-" * 80)
    print("Prove that different thread_ids maintain separate conversation memories.")
    print("Thread B should NOT have access to Thread A's conversation data.")
    
    # Create agent with memory
    print("\n🚀 Creating agent with InMemorySaver...")
    agent = create_attendance_agent(with_memory=True)
    print("✅ Agent created")
    
    # Create separate thread configurations
    config_a = create_thread_config("student-A")
    config_b = create_thread_config("student-B")
    
    print("\n✅ Thread configurations created:")
    print(f"   Thread A: thread_id='student-A'")
    print(f"   Thread B: thread_id='student-B'")
    
    # ========================================
    # THREAD A - TURN 1
    # ========================================
    print("\n" + "=" * 80)
    print("🧵 THREAD A - TURN 1: Provide attendance information")
    print("=" * 80)
    
    thread_a_msg1 = "I've attended 28 of 40 classes."
    print(f"\n👤 Student A: {thread_a_msg1}")
    
    result_a1 = agent.invoke(
        {"messages": [("user", thread_a_msg1)]},
        config=config_a  # Using Thread A config
    )
    
    print(f"\n🤖 Agent: {result_a1['messages'][-1].content[:100]}...")
    
    # Show tool call
    print("\n🔧 Thread A - Tool Call:")
    for msg in result_a1["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                args_str = ", ".join([f"{k}={v}" for k, v in tc['args'].items()])
                print(f"   {tc['name']}({args_str})")
    
    # ========================================
    # THREAD B - TURN 1
    # ========================================
    print("\n" + "=" * 80)
    print("🧵 THREAD B - TURN 1: Ask eligibility WITHOUT providing data")
    print("=" * 80)
    
    thread_b_msg1 = "Am I eligible?"
    print(f"\n👤 Student B: {thread_b_msg1}")
    print("\n⚠️  IMPORTANT: Student B did NOT provide any attendance data!")
    print("   Thread B should NOT have access to Thread A's data (28/40).")
    
    result_b1 = agent.invoke(
        {"messages": [("user", thread_b_msg1)]},
        config=config_b  # Using Thread B config (DIFFERENT from Thread A)
    )
    
    print(f"\n🤖 Agent: {result_b1['messages'][-1].content}")
    
    # Check if Thread B tried to use Thread A's data
    print("\n🔍 Thread B - Analysis:")
    print("-" * 80)
    
    tool_called_b = False
    for msg in result_b1["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            tool_called_b = True
            for tc in msg.tool_calls:
                print(f"⚠️  Tool called: {tc['name']}")
                print(f"   Args: {tc['args']}")
    
    if not tool_called_b:
        print("✅ CORRECT: No tool called (agent doesn't have attendance data)")
    else:
        print("⚠️  Tool was called - checking if it used Thread A's data...")
    
    # Check agent's response
    response_b = result_b1['messages'][-1].content.lower()
    if "provide" in response_b or "need" in response_b or "don't have" in response_b or "information" in response_b:
        print("✅ CORRECT: Agent asked for attendance information")
    elif "28" in response_b or "40" in response_b:
        print("❌ ERROR: Agent leaked Thread A's data!")
    
    # ========================================
    # THREAD A - TURN 2
    # ========================================
    print("\n" + "=" * 80)
    print("🧵 THREAD A - TURN 2: Ask eligibility (should remember 28/40)")
    print("=" * 80)
    
    thread_a_msg2 = "Am I eligible?"
    print(f"\n👤 Student A: {thread_a_msg2}")
    print("\n✅ Thread A should still remember the 28/40 from Turn 1")
    
    result_a2 = agent.invoke(
        {"messages": [("user", thread_a_msg2)]},
        config=config_a  # Back to Thread A config
    )
    
    print(f"\n🤖 Agent: {result_a2['messages'][-1].content[:100]}...")
    
    # Show tool call from Thread A Turn 2
    print("\n🔧 Thread A - Tool Call:")
    tool_args_a2 = None
    for msg in result_a2["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_args_a2 = tc['args']
                args_str = ", ".join([f"{k}={v}" for k, v in tc['args'].items()])
                print(f"   {tc['name']}({args_str})")
    
    # ========================================
    # VERIFICATION
    # ========================================
    print("\n" + "=" * 80)
    print("✅ THREAD ISOLATION VERIFICATION")
    print("=" * 80)
    
    print("\n📊 THREAD A SUMMARY:")
    print("-" * 80)
    print(f"   Total messages in Thread A: {len(result_a2['messages'])}")
    print(f"   Turn 1: Provided attendance (28/40)")
    print(f"   Turn 2: Asked eligibility")
    if tool_args_a2:
        print(f"   Turn 2 tool used: attended={tool_args_a2.get('attended')}, total={tool_args_a2.get('total')}")
        if tool_args_a2.get('attended') == 28 and tool_args_a2.get('total') == 40:
            print("   ✅ Thread A correctly remembered its own data")
    
    print("\n📊 THREAD B SUMMARY:")
    print("-" * 80)
    print(f"   Total messages in Thread B: {len(result_b1['messages'])}")
    print(f"   Turn 1: Asked eligibility WITHOUT data")
    
    # Check if Thread B stayed isolated
    thread_b_isolated = True
    thread_b_response = result_b1['messages'][-1].content
    
    if "28" in thread_b_response or "40" in thread_b_response or "70" in thread_b_response:
        thread_b_isolated = False
        print("   ❌ Thread B leaked data from Thread A")
    else:
        print("   ✅ Thread B correctly isolated (no access to Thread A's data)")
    
    # Final verification
    print("\n" + "=" * 80)
    print("🎯 ISOLATION TEST RESULT")
    print("=" * 80)
    
    if thread_b_isolated and tool_args_a2:
        if tool_args_a2.get('attended') == 28 and tool_args_a2.get('total') == 40:
            print("\n✅ SUCCESS: Thread isolation is working correctly!")
            print("   ✅ Thread A maintains its own conversation memory")
            print("   ✅ Thread B has separate, isolated memory")
            print("   ✅ No data leakage between threads")
    else:
        print("\n⚠️  Thread isolation may have issues - review results above")
    
    print("\n" + "=" * 80)
    print(" " * 28 + "PART 2 COMPLETE ✅")
    print("=" * 80)
    
    print("\n📝 KEY LEARNING:")
    print("   Different thread_ids create completely separate conversation memories.")
    print("   Each thread maintains its own state independently.")
    print("   This enables multi-user applications where each user has their own thread.")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    test_thread_isolation()
