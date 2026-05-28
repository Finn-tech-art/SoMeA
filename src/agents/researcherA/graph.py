# src/agents/researcherA/graph.py
"""
ResearcherA Agent Graph: Multi-stage research pipeline with parallel map-reduce.

Flow:
1. Radar Node (integration_prob): Discovers 5 trends
2. Parallel Enrichment via conditional_edges with Send routing
3. Reducer: Combines all enriched trends into unified state
4. Voice Node: Creates persona guidelines from enriched trends
5. Strategy Node: Frames B2B campaign strategy
"""

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from src.agents.researcherA.state import ResearcherALocalState
from src.agents.researcherA.nodes.integration_prob import integration_prob_node
from src.agents.researcherA.nodes.enrichment import (
    enrich_single_trend,
    reducer_combine_enrichments
)
from src.agents.researcherA.nodes.voice import voice_profiling_node
from src.agents.researcherA.nodes.strategy import campaign_strategy_node


def build_researcher_a_graph():
    """
    Constructs the LangGraph state machine with parallel enrichment via Send API.
    
    Uses conditional_edges from Radar to directly spawn parallel workers via Send().
    All workers complete, then reducer aggregates results.
    """
    graph = StateGraph(ResearcherALocalState)
    
    # ========== NODE DEFINITIONS ==========
    
    # Node 1: The Radar (Discover trends)
    graph.add_node("radar", integration_prob_node)
    
    # Node 2 Workers: Parallel enrichment (one instance per trend)
    def worker_wrapper(state):
        """Worker that enriches a single trend passed via state."""
        trend = state.get("trend", {})
        trigger_context = state.get("trigger_context", "")
        enriched = enrich_single_trend(trend, trigger_context)
        return {"enriched_trend_items": [enriched]}
    
    graph.add_node("enrich_worker", worker_wrapper)
    
    # Reducer: Combine all parallel results into enriched_trends list
    def reducer_node(state):
        """Reducer aggregates all enriched trends."""
        return reducer_combine_enrichments(state)
    
    graph.add_node("reducer", reducer_node)
    
    # Node 3: Voice Guidelines (from enriched trends)
    graph.add_node("voice", voice_profiling_node)
    
    # Node 4: Strategy Framing
    graph.add_node("strategy", campaign_strategy_node)
    
    # ========== ROUTING FUNCTIONS ==========
    
    def route_from_radar_to_workers(state: ResearcherALocalState):
        """
        Routes from Radar directly to parallel workers.
        Returns Send() commands for each trend to be enriched in parallel.
        """
        trends = state.get("synthesized_trends", [])
        macro_trigger = state.get("macro_trigger", "")
        
        if not trends:
            return "reducer"  # Skip to reducer if no trends
        
        # Return Send() commands for parallel execution
        return [
            Send("enrich_worker", {
                "trend": trend,
                "trigger_context": macro_trigger
            })
            for trend in trends
        ]
    
    # ========== EDGE DEFINITIONS (Control Flow) ==========
    
    # Start -> Radar (discover trends)
    graph.add_edge(START, "radar")
    
    # Radar -> Parallel Workers via Send() routing
    # conditional_edges properly handles Send() objects for parallel task routing
    graph.add_conditional_edges(
        "radar",
        route_from_radar_to_workers
    )
    
    # All parallel workers route to Reducer
    graph.add_edge("enrich_worker", "reducer")
    
    # Reducer -> Voice (analyze all enrichments for persona)
    graph.add_edge("reducer", "voice")
    
    # Voice -> Strategy (frame campaign from voice + enrichments)
    graph.add_edge("voice", "strategy")
    
    # Strategy -> End
    graph.add_edge("strategy", END)
    
    return graph.compile()


# Export for external usage
researcher_a_graph = build_researcher_a_graph()
