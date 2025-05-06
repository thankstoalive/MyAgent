from langgraph.graph import Graph
from backend.models.chat_state import ChatState
from backend.agents.intent_node import intent_parsing_node
from backend.agents.execute_fs_node import execute_fs_node
from backend.agents.respond_node import respond_node

def build_chat_graph() -> Graph:
    """
    Build and compile the LangGraph workflow for chat-based filesystem agent.
    Returns a compiled graph runnable that transforms ChatState through intents,
    filesystem execution, and response generation.
    """
    graph = Graph()
    # Add nodes: intent parsing, filesystem execution, response
    graph.add_node(intent_parsing_node)
    graph.add_node(execute_fs_node)
    graph.add_node(respond_node)
    # Connect nodes sequentially: START -> Intent -> Exec -> Respond -> END
    graph.set_entry_point(intent_parsing_node.__name__)
    graph.add_edge(intent_parsing_node.__name__, execute_fs_node.__name__)
    graph.add_edge(execute_fs_node.__name__, respond_node.__name__)
    graph.set_finish_point(respond_node.__name__)
    # Compile into runnable
    compiled = graph.compile()
    return compiled