"""
MILESTONE 5: Tool Call Tracing Demonstration

This demonstrates the trace helper functions that show exactly
what the model generated, including all tool call arguments.
"""

from src.agent import create_attendance_agent
from src.memory import create_thread_config
from src.trace import print_trace, print_tool_calls_only, print_compact_trace


def test_trace_single_turn():
    """Test tracing with a single-turn conversation."""
    print("\n" + "=" * 80)
    print(" " * 20 + "MILESTONE 5: TOOL CALL TRACING")
    print("=" * 80)
    
    print("\n📋 TEST 1: Single-Turn Conversation")
    print("=" * 80)
    
    # Create agent
    agent = create_attendance_agent(with_memory=False)
    
    # Test question
    question = "I attended 28 out of 40 classes. Am I eligible?"
    print(f"\n❓ Question: {question}")
    
    # Invoke agent
    result = agent.invoke({"messages": [("user", question)]})
    
    # Show different trace formats
    print_trace(result, "FULL DETAILED TRACE")
    print_tool_calls_only(result)
    print_compact_trace(result)
    
    print("\n✅ Test 1 Complete\n")


def test_trace_multi_turn():
    """Test tracing with multi-turn conversation."""
    print("=" * 80)
    print("📋 TEST 2: Multi-Turn Conversation with Memory")
    print("=" * 80)
    
    # Create agent with memory
    agent = create_attendance_agent(with_memory=True)
    config = create_thread_config("trace-test")
    
    # Turn 1
    print("\n🔵 TURN 1:")
    turn1 = "I've attended 28 of 40 classes."
    print(f"   {turn1}")
    
    result1 = agent.invoke({"messages": [("user", turn1)]}, config=config)
    print_compact_trace(result1)
    
    # Turn 2
    print("\n🔵 TURN 2:")
    turn2 = "Am I eligible?"
    print(f"   {turn2}")
    
    result2 = agent.invoke({"messages": [("user", turn2)]}, config=config)
    
    # Show full trace of Turn 2
    print_trace(result2, "TURN 2 DETAILED TRACE")
    
    # Extract and highlight tool calls
    print("\n🎯 TOOL CALL VERIFICATION:")
    print("-" * 80)
    
    for msg in result2["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc['name'] == 'check_attendance_eligibility':
                    args = tc['args']
                    print(f"✅ Tool: {tc['name']}")
                    print(f"   Arguments from memory:")
                    print(f"      attended = {args.get('attended')} (from Turn 1)")
                    print(f"      total = {args.get('total')} (from Turn 1)")
    
    print("-" * 80)
    print("\n✅ Test 2 Complete\n")


def test_trace_different_tool():
    """Test tracing with the classes_needed_for_eligibility tool."""
    print("=" * 80)
    print("📋 TEST 3: Different Tool Call")
    print("=" * 80)
    
    # Create agent
    agent = create_attendance_agent(with_memory=False)
    
    # Question that should trigger classes_needed_for_eligibility
    question = "I attended 28 of 40 classes. If 20 classes remain, how many more do I need to attend?"
    print(f"\n❓ Question: {question}")
    
    # Invoke agent
    result = agent.invoke({"messages": [("user", question)]})
    
    # Show trace
    print_trace(result, "CLASSES NEEDED TOOL TRACE")
    
    # Highlight the specific tool call
    print("\n🎯 TOOL CALL DETAILS:")
    print("-" * 80)
    
    for msg in result["messages"]:
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"Tool Name: {tc['name']}")
                print(f"Tool Arguments: {tc['args']}")
                print(f"\nFormatted:")
                args_str = ", ".join([f"{k}={v}" for k, v in tc['args'].items()])
                print(f"   {tc['name']}({args_str})")
    
    print("-" * 80)
    print("\n✅ Test 3 Complete\n")


def main():
    """Run all trace tests."""
    print("\n" + "=" * 80)
    print(" " * 15 + "MILESTONE 5: AGENT TOOL CALL TRACING")
    print("=" * 80)
    
    print("\n🎯 PURPOSE:")
    print("-" * 80)
    print("Create helper functions to inspect exactly what the model generated,")
    print("including all tool calls and their exact arguments.")
    print("This is essential for debugging and verifying memory behavior.")
    
    # Run tests
    test_trace_single_turn()
    test_trace_multi_turn()
    test_trace_different_tool()
    
    # Summary
    print("=" * 80)
    print(" " * 25 + "MILESTONE 5 COMPLETE ✅")
    print("=" * 80)
    
    print("\n✅ TRACE FUNCTIONS CREATED:")
    print("   1. print_trace() - Full detailed trace")
    print("   2. print_tool_calls_only() - Only tool calls")
    print("   3. print_compact_trace() - Compact summary")
    
    print("\n✅ USE CASES:")
    print("   - Verify tool calls are happening")
    print("   - Inspect exact tool arguments")
    print("   - Debug memory retrieval")
    print("   - Understand agent decision flow")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
