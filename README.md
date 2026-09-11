# Attendence.io

**Conversational AI Attendance Eligibility Agent**

A LangGraph-based intelligent agent that demonstrates conversational memory and multi-turn tool calling. The agent helps students check their attendance eligibility and calculate how many classes they need to attend to meet the 75% requirement.

---

##  Overview

This project is a learning implementation focused on **LangGraph's conversation memory capabilities** using the `InMemorySaver` checkpointer. It demonstrates how an AI agent can remember information from earlier conversation turns and use that information to make intelligent tool calls later, without users needing to repeat themselves.

### Key Learning Objectives

✅ **Conversational Memory** - Agent remembers context across multiple turns  
✅ **Thread Isolation** - Separate conversations maintain independent memories  
✅ **Multi-Turn Tool Calling** - Memory affects tool invocation and arguments  
✅ **Natural Interactions** - Users don't need to repeat information

---

##  Features

- ** Conversational Memory**: Remembers attendance information across multiple conversation turns
- ** Intelligent Tool Calling**: Automatically decides when to use tools based on conversation context
- ** Thread Isolation**: Multiple conversations with separate, isolated memories
- ** Attendance Checking**: Verifies if students meet the 75% attendance requirement
- ** Planning Tool**: Calculates how many classes must be attended to reach eligibility
- ** Trace Utilities**: Debug and inspect agent behavior and tool calls

---

##  Architecture

### Tech Stack

- **Python 3.10+**
- **LangChain** - Framework for building LLM applications
- **LangGraph** - Orchestration library for multi-step agent workflows
- **ChatOllama** - Local LLM integration (qwen2.5:3b)
- **InMemorySaver** - Conversation state persistence

### System Design

```
┌─────────────────────────────────────────────────┐
│                   User Input                    │
└───────────────────┬─────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│              LangGraph Agent                    │
│  ┌──────────────────────────────────────────┐  │
│  │         MessagesState                    │  │
│  │  (Conversation History)                  │  │
│  └──────────────────────────────────────────┘  │
│                    ↓                            │
│  ┌──────────────────────────────────────────┐  │
│  │    ChatOllama (qwen2.5:3b)              │  │
│  │    - Analyzes conversation               │  │
│  │    - Decides tool usage                  │  │
│  └──────────────────────────────────────────┘  │
│                    ↓                            │
│  ┌──────────────────────────────────────────┐  │
│  │        tools_condition                   │  │
│  │    (Routing: tools or END)               │  │
│  └──────────────────────────────────────────┘  │
│                    ↓                            │
│  ┌──────────────────────────────────────────┐  │
│  │          ToolNode                        │  │
│  │  - check_attendance_eligibility          │  │
│  │  - classes_needed_for_eligibility        │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│           InMemorySaver Checkpointer            │
│     (Persists conversation state by thread)     │
└─────────────────────────────────────────────────┘
```

### Graph Flow

```
START → agent → tools_condition → tools → agent → END
         ↑                                   ↓
         └───────────────────────────────────┘
```

---

## 📁 Project Structure

```
Attendence.io/
│
├── src/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # LangGraph agent implementation
│   ├── tools.py             # Attendance checking tools
│   ├── memory.py            # Memory utilities (thread config, state display)
│   └── trace.py             # Tracing utilities for debugging
│
├── tests/
│   ├── __init__.py
│   └── test_tools.py        # Tool unit tests
│
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
│
├── test_memory_part1.py     # Part 1: Basic memory test
├── test_thread_isolation.py # Part 2: Thread isolation test
├── test_capstone.py         # Part 3: Multi-turn tool calling test
├── test_trace.py            # Trace utilities demonstration
├── verify_tools.py          # Tool verification script
│
└── milestone*_summary.py    # Milestone demonstrations
```

---

##  Setup

### Prerequisites

1. **Python 3.10 or higher**
2. **Ollama** with `qwen2.5:3b` model

### Installation

```bash
# Clone the repository
git clone https://github.com/rahultakale44/Attendence.io.git
cd Attendence.io

# Install dependencies
pip install -r requirements.txt
```

### Ollama Setup

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai

# Pull the qwen2.5:3b model
ollama pull qwen2.5:3b

# Verify installation
ollama list
```

---

##  Running the Project

### Quick Start

```bash
# Run the main demonstration
python main.py
```

### Run Individual Tests

```bash
# Test Part 1: Basic conversation memory
python test_memory_part1.py

# Test Part 2: Thread isolation
python test_thread_isolation.py

# Test Part 3: Capstone - Multi-turn tool calling
python test_capstone.py

# Test tracing utilities
python test_trace.py

# Verify tools
python verify_tools.py
```

### Run Milestone Summaries

```bash
python milestone3_summary.py  # Basic LangGraph agent
python milestone4_summary.py  # Conversation memory
python milestone5_summary.py  # Tool call tracing
python milestone6_summary.py  # Thread isolation
python milestone7_summary.py  # Capstone demonstration
```

---

##  Learning Progression

### Part 1: Conversation Memory

**Objective**: Demonstrate basic memory across turns using `InMemorySaver` and `thread_id`.

**Example**:
```
Turn 1: "I've attended 28 of 40 classes."
Turn 2: "Am I eligible?"  ← Does not repeat 28 or 40

Result: Agent remembers 28/40 and answers correctly
```

**Key Concepts**:
- `InMemorySaver` checkpointer
- `thread_id` for conversation continuity
- `MessagesState` persistence

**Run**: `python test_memory_part1.py`

---

### Part 2: Thread Isolation

**Objective**: Prove that different `thread_id` values create separate memories.

**Example**:
```
Thread A: "I've attended 28 of 40 classes."
Thread B: "Am I eligible?"  ← Different thread_id

Result: Thread B does NOT have access to Thread A's data
```

**Key Concepts**:
- Thread isolation
- Memory separation
- Multi-user capability

**Run**: `python test_thread_isolation.py`

---

### Part 3: Multi-Turn Tool Calling (Capstone)

**Objective**: Information from Turn 1 is used to populate tool arguments in Turn 2.

**Example**:
```
Turn 1: "I've attended 28 of 40 classes so far."
Turn 2: "If 20 classes remain this semester, how many more do I need?"
        ↑ Does NOT mention 28 or 40!

Agent Tool Call:
  classes_needed_for_eligibility(
    attended=28,           ← from Turn 1 memory
    total_so_far=40,       ← from Turn 1 memory
    remaining_classes=20   ← from Turn 2 input
  )

Result: "You need to attend 17 more classes out of 20 remaining."
```

**Key Concepts**:
- Memory affects tool calling
- Context-aware tool invocation
- Multi-turn intelligence

**Run**: `python test_capstone.py`

---

##  Trace Verification

The project includes tracing utilities to inspect agent behavior:

```python
from src.trace import print_trace, print_tool_calls_only, print_compact_trace

# Full detailed trace
print_trace(result, "My Trace")

# Only tool calls
print_tool_calls_only(result)

# Compact summary
print_compact_trace(result)
```

**Example Output**:
```
[0]  User: I attended 28 of 40 classes. Am I eligible?
[1]  AI -> 🔧 check_attendance_eligibility(attended=28, total=40)
[2]  Tool: NOT ELIGIBLE: 70.0% attendance (below 75%).
[3]  AI: Based on the information provided, you have 70.0% attendance...
```

---

##  Key Learnings

### 1. MessagesState

LangGraph's built-in state management:
- Stores conversation history
- Contains all messages: `HumanMessage`, `AIMessage`, `ToolMessage`
- Automatically managed by the graph

### 2. LangGraph

Orchestration framework for agents:
- `StateGraph` - Defines agent workflow
- `ToolNode` - Automatic tool execution
- `tools_condition` - Intelligent routing
- Conditional edges for decision-making

### 3. Checkpointer (InMemorySaver)

Conversation state persistence:
- Stores state between invocations
- Enables multi-turn conversations
- Thread-based isolation
- **Note**: InMemorySaver is for development/testing only, not production

### 4. thread_id

Conversation identification:
- Unique identifier for each conversation thread
- Same `thread_id` = shared memory
- Different `thread_id` = isolated memory
- Enables multi-user applications

### 5. State Persistence

How memory works:
- Each `agent.invoke()` saves state via checkpointer
- Next invocation loads previous state
- LLM sees full conversation history
- Memory affects tool calling decisions

### 6. Thread Isolation

Memory separation:
- Each thread has independent memory
- No data leakage between threads
- Perfect for multi-user scenarios
- Clean testing without interference

### 7. Tool Calling

Intelligent tool usage:
- LLM decides when tools are needed
- LLM generates tool arguments
- Memory influences tool invocation
- Combines past context + current input

### 8. Context Retention

Multi-turn intelligence:
- Users don't repeat information
- Agent references earlier turns
- Natural conversation flow
- Context-aware responses

---

##  Important Notes

### InMemorySaver Limitations

⚠️ **InMemorySaver is NOT for production use**

- **Development/Testing Only**: Great for learning and local development
- **Not Persistent**: Data lost when program terminates
- **Not Scalable**: Stored in process memory only
- **No Distribution**: Cannot share across instances

**For Production**, use:
- `PostgresSaver` - PostgreSQL-backed persistence
- `SqliteSaver` - SQLite-backed persistence  
- Custom implementations for Redis, MongoDB, etc.

---

##  Testing

```bash
# Run tool tests
python tests/test_tools.py

# All tests passed ✅
```

---

##  Contributing

This is a learning project. Feel free to:
- Explore the code
- Experiment with different scenarios
- Extend with new features
- Learn from the implementation

---

##  License

This project is for educational purposes.

---

##  Acknowledgments

- **LangChain** - For the amazing framework
- **LangGraph** - For conversation memory capabilities
- **Ollama** - For local LLM execution
- **qwen2.5:3b** - For the efficient language model

---

##  Contact

**GitHub**: [rahultakale44/Attendence.io](https://github.com/rahultakale44/Attendence.io)

---

**Built with ❤️ to learn LangGraph conversation memory**
