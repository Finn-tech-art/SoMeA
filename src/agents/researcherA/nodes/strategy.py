"""Synthesizes findings into a formal case study layout matching one of your 24 software core assets."""

# src/agents/researcherA/nodes/strategy.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict
from langchain_groq import ChatGroq
from src.agents.researcherA.state import ResearcherALocalState

load_dotenv()

# --- STRUCTURED CAMPAIGN STRATEGY SCHEMA ---
class PlatformInstruction(BaseModel):
    format_focus: str = Field(description="The structural focus for this platform (e.g., '10-part tactical thread', 'Short text status with code snippet').")
    core_argument: str = Field(description="The primary message this platform must deliver to the reader.")

class CampaignStrategySchema(BaseModel):
    master_campaign_angle: str = Field(description="The core narrative thesis connecting the trend to real-world impact.")
    key_narrative_pillars: List[str] = Field(description="3 distinct educational or philosophical points to argue across posts.")
    platform_blueprints: Dict[str, PlatformInstruction] = Field(description="Platform-specific content direction mapping platform name to instructions.")

# --- NODE IMPLEMENTATION ---
def campaign_strategy_node(state: ResearcherALocalState) -> dict:
    """
    Agent 1, Node 4: The Strategist.
    Consumes selected trends, enriched context data fuel, and voice guidelines 
    to map out a cross-platform narrative strategy.
    """
    trend = state.get("selected_trend")
    context = state.get("enriched_context")
    voice = state.get("voice_guidelines")
    
    if not trend or not context or not voice:
        return {"campaign_strategy": "Insufficient data to build campaign strategy."}
        
    llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.4)
    structured_strategist = llm.with_structured_output(CampaignStrategySchema)
    
    system_prompt = (
        "You are an Expert B2B Content Strategist specializing in technical developer relations. "
        "Your task is to take deep engineering context and a specific human voice profile, and compile "
        "a cross-platform distribution campaign blueprint for X, facebook, linkedIn, instagram carousels, . Ensure the strategy feels cohesive across channels.\n\n"
        f"SELECTED TREND: {trend['thematic_title']}\n"
        f"VOICE PROFILE: {voice['persona_title']} (Directives: {', '.join(voice['tone_profile'])})\n\n"
        f"RAW TECHNICAL MASS:\n{context[:3000]}"
    )
    
    # Generate structured multi-platform strategy
    strategy_payload = structured_strategist.invoke(system_prompt)
    
    # Convert structured object to dictionary for clean state migration
    strategy_blueprint = {
        "master_campaign_angle": strategy_payload.master_campaign_angle,
        "key_narrative_pillars": strategy_payload.key_narrative_pillars,
        "platform_blueprints": {
            platform: {"format_focus": inst.format_focus, "core_argument": inst.core_argument}
            for platform, inst in strategy_payload.platform_blueprints.items()
        }
    }
    
    return {
        "campaign_strategy": strategy_blueprint
    }