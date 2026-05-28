# src/agents/researcherA/nodes/enrichment.py
import os
import requests
from langchain_groq import ChatGroq
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from src.agents.researcherA.state import ResearcherALocalState
from dotenv import load_dotenv

load_dotenv()

def jina_reader_fetch(url: str, timeout: int = 15) -> str:
    """
    Fetches a URL using Jina Reader API (https://r.jina.ai/).
    Handles JavaScript-rendered content, login walls, and returns pristine Markdown.
    No API key required.
    """
    try:
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return response.text
        return ""
    except Exception as e:
        return f"[Jina Reader fetch failed: {str(e)}]"

def technical_enrichment_node(state: ResearcherALocalState) -> dict:
    """
    Agent 1, Node 2: The Excavator (Enhanced).
    Consumes discovered insights from Node 1, isolates a target topic, 
    and harvests full documentation/reference material from world-class engineering hubs using Jina Reader.
    
    Evolution B: Domain-constrained queries targeting trusted engineering sources.
    Evolution C: Jina Reader API for robust content extraction (handles JS, login walls, proxies).
    """
    trends = state.get("synthesized_trends", [])
    if not trends:
        return {"selected_trend": None, "enriched_context": "No trends found to enrich."}
    
    # 1. Topic Selection Step (Lock onto the primary trend)
    chosen_trend = trends[0]
    
    # 2. Build precision deep-harvest query with domain constraints
    # Force search to look exclusively at world-class engineering blogs and trusted hubs
    trusted_hubs = (
        "(site:netflixtechblog.com OR site:engineering.fb.com OR site:github.blog OR "
        "site:aws.amazon.com/blogs/architecture OR site:cloudblog.google OR site:engineering.shopify.com)"
    )
    deep_query = (
        f'"{chosen_trend["thematic_title"]}" {chosen_trend["underlying_cause"]} '
        f'engineering documentation {trusted_hubs}'
    )
    
    search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.1)
    
    deep_context_buffer = ""
    
    try:
        search_links = search_wrapper.results(deep_query, max_results=2)
        for link_item in search_links:
            url = link_item.get("link")
            if not url:
                continue
            
            # Use Jina Reader for robust content extraction
            fetched_content = jina_reader_fetch(url)
            if fetched_content and len(fetched_content) > 100:
                deep_context_buffer += f"\n--- REFERENCE CONTENT FROM {url} ---\n{fetched_content[:5000]}\n"
    except Exception as e:
        deep_context_buffer = f"Domain-constrained harvest completed with fallback. Trace: {str(e)}"
        
    # Expert generation fallback if live pages yield insufficient text mass
    if len(deep_context_buffer.strip()) < 200:
        fallback_prompt = (
            "You are a Senior Principal Systems Engineer. Generate a comprehensive internal technical "
            "reference guide detailing the architectural mechanics, code blocks, real-world failure states, "
            f"and resolution strategies for this precise issue:\n\n"
            f"Topic: {chosen_trend['thematic_title']}\n"
            f"Root Cause: {chosen_trend['underlying_cause']}"
        )
        deep_context_buffer = llm.invoke(fallback_prompt).content

    # CRITICAL FIX: The dictionary key must exactly match the state definition
    return {
        "selected_trend": chosen_trend,
        "enriched_context": deep_context_buffer  # <-- Change from enriched_technical_context
    }


def enrich_single_trend(trend: dict, trigger_context: str = "") -> dict:
    """
    MAP WORKER: Enriches a single trend in parallel.
    Called once per trend via Send() in dispatcher.
    
    Returns enriched context for that specific trend.
    """
    from src.agents.researcherA.state import EnrichedTrend
    
    search_wrapper = DuckDuckGoSearchAPIWrapper(max_results=3)
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.1)
    
    # Build domain-constrained query
    trusted_hubs = (
        "(site:netflixtechblog.com OR site:engineering.fb.com OR site:github.blog OR "
        "site:aws.amazon.com/blogs/architecture OR site:cloudblog.google OR site:engineering.shopify.com)"
    )
    deep_query = (
        f'"{trend["thematic_title"]}" {trend["underlying_cause"]} '
        f'engineering documentation {trusted_hubs}'
    )
    
    deep_context_buffer = ""
    
    try:
        search_links = search_wrapper.results(deep_query, max_results=2)
        for link_item in search_links:
            url = link_item.get("link")
            if not url:
                continue
            
            fetched_content = jina_reader_fetch(url)
            if fetched_content and len(fetched_content) > 100:
                deep_context_buffer += f"\n--- REFERENCE CONTENT FROM {url} ---\n{fetched_content[:5000]}\n"
    except Exception as e:
        deep_context_buffer = f"Parallel enrichment network trace: {str(e)}"
        
    # Fallback if no content
    if len(deep_context_buffer.strip()) < 200:
        fallback_prompt = (
            "You are a Senior Principal Systems Engineer. Generate a comprehensive internal technical "
            "reference guide detailing the architectural mechanics, code blocks, real-world failure states, "
            f"and resolution strategies for this precise issue:\n\n"
            f"Topic: {trend['thematic_title']}\n"
            f"Root Cause: {trend['underlying_cause']}"
        )
        deep_context_buffer = llm.invoke(fallback_prompt).content
    
    enriched: EnrichedTrend = {
        "trend": trend,
        "enriched_context": deep_context_buffer
    }
    
    return enriched


def dispatcher_parallel_enrichment(state: ResearcherALocalState) -> list:
    """
    DISPATCHER: Spawns parallel enrichment tasks for all discovered trends.
    Uses LangGraph Send API to map each trend to parallel worker.
    
    Returns a list of Send() commands to route each trend.
    """
    from langgraph.types import Send
    
    trends = state.get("synthesized_trends", [])
    if not trends:
        return []
    
    # Send each trend to parallel enrichment worker
    return [
        Send("enrich_worker", {"trend": trend, "trigger_context": state.get("macro_trigger", "")})
        for trend in trends
    ]


def reducer_combine_enrichments(state: ResearcherALocalState) -> dict:
    """
    REDUCER: Combines all parallel-enriched trends into a unified state.
    Stores as enriched_trends list for downstream pipeline and also sets
    legacy single-trend keys for existing downstream nodes.
    """
    enriched_trends = state.get("enriched_trend_items", [])
    first_trend = enriched_trends[0] if enriched_trends else None
    return {
        "enriched_trends": enriched_trends,
        "selected_trend": first_trend["trend"] if first_trend else None,
        "enriched_context": first_trend["enriched_context"] if first_trend else None,
    }