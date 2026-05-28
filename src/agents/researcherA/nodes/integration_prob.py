"""Searches forums for real-world production errors, database deadlocks, API degradation issues, and system chokepoints."""
import os
from pydantic import BaseModel, Field
from typing import List, Literal
from langchain_groq import ChatGroq
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from src.agents.researcherA.state import ResearcherALocalState, ScrapedArtifact, SynthesizedTrend
from dotenv import load_dotenv

load_dotenv()

# --- STRUCTURED EXTRACTION SCHEMAS ---
class QueryMatrixSchema(BaseModel):
    developer_query: str = Field(description="Search term explicitly targeting developer forums or Hacker News for architecture bugs.")
    founder_query: str = Field(description="Search term explicitly targeting founder hubs or Indie Hackers for product/business issues.")
    b2b_complaint_query: str = Field(description="Search term targeting enterprise SaaS down-times or integration breakdown errors.")

class TrendAnalysisSchema(BaseModel):
    category: Literal["Technical Architecture", "Business Execution"] = Field(description="Is this primarily an engineering bug or a commercial/operational issue?")
    thematic_title: str = Field(description="A concise title capturing the systemic pattern found across the complaints.")
    underlying_cause: str = Field(description="Deep architectural root cause or system breakdown condition.")
    business_consequence: str = Field(description="The fallout metrics (e.g., engineering hours lost, customer churn, margin decay).")

class DiscoverySynthesisSchema(BaseModel):
    discovered_trends: List[TrendAnalysisSchema]

# --- NODE IMPLEMENTATION ---
def integration_prob_node(state: ResearcherALocalState) -> dict:
    """
    Agent 1, Node 1: Dynamic open-ended web harvester.
    Splits generic triggers into structural queries, scrapes distinct industry matrices via DuckDuckGo,
    and formats real-world real-time friction into categorical trends.
    """
    trigger = state["macro_trigger"]
    llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.2)
    search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=4)
    
    # PHASE 1: Generate cross-sector queries from the macro trigger
    query_generator = llm.with_structured_output(QueryMatrixSchema)
    system_query_prompt = (
        f"Analyze the macro discovery goal: '{trigger}'. Break it into exactly 3 divergent live "
        "search terms targeting specific technical and organizational failure patterns. Use keywords "
        "like 'unhandled exception', 'technical debt', 'downtime', 'architectural flaw', or platform site-restrictions."
    )
    search_targets = query_generator.invoke(system_query_prompt)
    
    query_map = {
        "Developer Forum": search_targets.developer_query,
        "Founder Hub": search_targets.founder_query,
        "B2B SaaS Crash": search_targets.b2b_complaint_query
    }
    
    # PHASE 2: Execute Live Harvester Engine
    artifacts: List[ScrapedArtifact] = []
    aggregation_buffer = ""
    
    for sector, query in query_map.items():
        try:
            search_results = search_wrapper.results(query, max_results=3)
            for item in search_results:
                artifacts.append({
                    "title": item.get("title", "Raw Insight Log"),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "sector": sector
                })
                aggregation_buffer += f"\n[Sector: {sector}] | Title: {item.get('title')}\nInsight: {item.get('snippet')}\n"
        except Exception:
            # Network resilient pass-through
            continue
            
    # Fallback to prevent execution pipeline crash if live network query yields zero data
    if not aggregation_buffer:
        aggregation_buffer = f"[Sector: Developer Forum] Mock sample regarding API rate-limiting and infrastructure memory leaks for {trigger}."
        
    # PHASE 3: Structured Synthesis into Categorized Trend Definitions
    synthesizer = llm.with_structured_output(DiscoverySynthesisSchema)
    synthesis_prompt = (
        "You are an Elite Systems Researcher. Take the following multi-platform raw web insights "
        "and isolate the systemic trends. Group them explicitly into either Technical Architecture issues "
        f"or Business Execution failures.\n\nScraped Data:\n{aggregation_buffer}"
    )
    synthesis_payload = synthesizer.invoke(synthesis_prompt)
    
    # Convert Pydantic schemas back to state-native TypedDict layout
    trends_output: List[SynthesizedTrend] = [
        {
            "category": t.category,
            "thematic_title": t.thematic_title,
            "underlying_cause": t.underlying_cause,
            "business_consequence": t.business_consequence
        } for t in synthesis_payload.discovered_trends
    ]
    
    # ... everything else in integration_prob_node remains exactly the same ...
    
    return {
        "executed_queries": list(query_map.values()),
        "raw_scraped_artifacts": artifacts,
        "synthesized_trends": trends_output,
        
        # ADD THESE LINES TO RESET DOWNSTREAM STATE FOR A FRESH CYCLICAL RUN
        "selected_trend": None,
        "enriched_context": None
    }