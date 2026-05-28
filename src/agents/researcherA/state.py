import operator
from typing import TypedDict, Optional, List, Dict, Annotated

class ScrapedArtifact(TypedDict):
    title: str
    url: str
    snippet: str
    sector: str  # "Developer Forum", "Founder Hub", or "B2B SaaS Crash"

class SynthesizedTrend(TypedDict):
    category: str             # "Technical Architecture" or "Business Execution"
    thematic_title: str       # e.g., "Database connection starvation under Serverless scale"
    underlying_cause: str     # The engineering or systemic root cause
    business_consequence: str # Impact on churn, cost, delivery speeds, or revenue

class EnrichedTrend(TypedDict):
    """Represents a single trend paired with its enriched context."""
    trend: SynthesizedTrend
    enriched_context: str

class ResearcherALocalState(TypedDict):
    # ==========================================
    # 1. INPUT STAGE (Trigger)
    # ==========================================
    macro_trigger: str                       # e.g., "Software industry production bottlenecks 2026"
    
    # ==========================================
    # 2. NODE 1 OUTPUTS (The Radar)
    # ==========================================
    executed_queries: List[str]
    raw_scraped_artifacts: List[ScrapedArtifact]
    synthesized_trends: List[SynthesizedTrend]
    
    # ==========================================
    # 3. INTEGRATION LAYER ADDITIONS (The Excavator - Map-Reduce)
    # ==========================================
    selected_trend: Optional[SynthesizedTrend]  # Single trend for sequential processing (legacy)
    enriched_context: Optional[str]            # Single enriched context (legacy)
    enriched_trend_items: Annotated[List[EnrichedTrend], operator.add]
    enriched_trends: Optional[List[EnrichedTrend]]  # Multiple parallel-enriched trends (new)
    
    # ==========================================
    # 4. DOWNSTREAM TARGETS (Voice & Strategy)
    # ==========================================
    voice_guidelines: Optional[dict]
    campaign_strategy: Optional[dict]