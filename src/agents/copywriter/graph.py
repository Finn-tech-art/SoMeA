from langgraph.graph import StateGraph, START, END
from src.agents.copywriter.state import CopywriterState
from src.agents.copywriter.nodes.copybrief import copy_brief_node
from src.agents.copywriter.nodes.x import copy_x_node
from src.agents.copywriter.nodes.linkedin import copy_linkedin_node
from src.agents.copywriter.nodes.insta import copy_insta_node
from src.agents.copywriter.nodes.tiktok import copy_tiktok_node
from src.agents.copywriter.nodes.facebook import copy_facebook_node


def build_copywriter_graph():
    """Builds the Copywriter state graph for campaign copy generation."""
    graph = StateGraph(CopywriterState)

    graph.add_node("copy_brief", copy_brief_node)
    graph.add_node("copy_x", copy_x_node)
    graph.add_node("copy_linkedin", copy_linkedin_node)
    graph.add_node("copy_insta", copy_insta_node)
    graph.add_node("copy_tiktok", copy_tiktok_node)
    graph.add_node("copy_facebook", copy_facebook_node)

    graph.add_edge(START, "copy_brief")
    graph.add_edge("copy_brief", "copy_x")
    graph.add_edge("copy_brief", "copy_linkedin")
    graph.add_edge("copy_brief", "copy_insta")
    graph.add_edge("copy_brief", "copy_tiktok")
    graph.add_edge("copy_brief", "copy_facebook")
    graph.add_edge([
        "copy_x",
        "copy_linkedin",
        "copy_insta",
        "copy_tiktok",
        "copy_facebook",
    ], END)

    return graph.compile()


copywriter_graph = build_copywriter_graph()
