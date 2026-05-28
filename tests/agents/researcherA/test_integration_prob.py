import pytest
from src.agents.researcherA.state import ResearcherALocalState
from src.agents.researcherA.nodes.integration_prob import integration_prob_node

def test_integration_prob_node_broad_discovery_contract():
    """
    Unit test for Agent 1, Node 1.
    Verifies that passing a generic macro trigger initiates a multi-sector 
    live scrape and correctly extracts structured technical & operational vectors.
    """
    # 1. Arrange: Setup broad unconstrained trigger input
    initial_state: ResearcherALocalState = {
        "macro_trigger": "SaaS industry technical debt and developer infrastructure complaints",
        "executed_queries": [],
        "raw_scraped_artifacts": [],
        "synthesized_trends": [],
        "voice_guidelines": None,
        "campaign_strategy": None
    }
    
    # 2. Act: Run the node
    mutated_state = integration_prob_node(initial_state)
    
    # 3. Assert: Structural and Data Schema Contract Validations
    assert "executed_queries" in mutated_state
    assert "raw_scraped_artifacts" in mutated_state
    assert "synthesized_trends" in mutated_state
    
    # Verify the node did not target just one domain, but expanded its search horizon
    assert len(mutated_state["executed_queries"]) >= 3, "Node failed to split search vectors."
    assert len(mutated_state["raw_scraped_artifacts"]) > 0, "No live search results collected."
    assert len(mutated_state["synthesized_trends"]) > 0, "Failed to analyze or synthesize trends."
    
    # Verify data types and nested properties inside the list contracts
    first_trend = mutated_state["synthesized_trends"][0]
    assert "category" in first_trend
    assert first_trend["category"] in ["Technical Architecture", "Business Execution"]
    assert "thematic_title" in first_trend
    assert "underlying_cause" in first_trend
    assert "business_consequence" in first_trend
    
    print(f"\n\n🟩 [BROAD SCOPE SCRAPE PASSED]")
    print(f"Fired Queries: {mutated_state['executed_queries']}")
    print(f"Discovered Matrix Sample: {first_trend['thematic_title']} ({first_trend['category']})")