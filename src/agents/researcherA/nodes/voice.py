# src/agents/researcherA/nodes/voice.py
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from src.agents.researcherA.state import ResearcherALocalState

load_dotenv()

# --- STRUCTURED OUTGOING GUARDRAILS SCHEMA ---
class VoiceGuardrailsSchema(BaseModel):
    persona_title: str = Field(description="The professional identity assumed (e.g., 'Cynical Principal Architect', 'Bootstrapped SaaS Founder').")
    tone_profile: List[str] = Field(description="3 to 5 stylistic tone directives (e.g., 'punchy sentences', 'dev-to-dev empathy', 'no corporate jargon').")
    banned_phrases: List[str] = Field(description="Explicit AI/marketing clichés to completely outlaw from generation (e.g., 'delve', 'revolutionize', 'unleash').")
    narrative_hook_style: str = Field(description="Instructions on how this persona opens a post (e.g., 'Start mid-crisis with a specific engineering failure metric').")
    technical_density_rule: str = Field(description="Directive on how to blend deep code/architecture specs with high-level readability.")

# --- NODE IMPLEMENTATION ---
def voice_profiling_node(state: ResearcherALocalState) -> dict:
    """
    Agent 1, Node 3: The Sculptor (voice.py).
    Consumes raw technical excavation text and builds architectural style guardrails 
    to force downstream copywriters to sound like highly authentic, specific humans.
    """
    trend = state.get("selected_trend")
    context = state.get("enriched_context")
    
    if not trend or not context:
        return {
            "voice_guidelines": {
                "persona_title": "Standard Industry Analyst",
                "tone_profile": ["informative", "professional", "standard pacing"],
                "banned_phrases": ["delve", "testament", "game-changing"],
                "narrative_hook_style": "Direct problem statement.",
                "technical_density_rule": "Maintain basic text clarity."
            }
        }
        
    llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.3)
    structured_profiler = llm.with_structured_output(VoiceGuardrailsSchema)
    
    system_prompt = (
        "You are an Elite Brand Strategist and Copywriting Director. Your job is to review raw engineering "
        "failure logs/documentation and create an ultra-authentic social media voice profile. "
        "The copy generated from this profile MUST read like a real human writing on a forum or timeline—never generic AI.\n\n"
        f"TARGET TOPIC:\nTitle: {trend['thematic_title']}\nRoot Cause: {trend['underlying_cause']}\n\n"
        f"RAW DATA FUEL CONTEXT:\n{context[:4000]}"
    )
    
    # Generate structured profile boundaries
    guidelines_payload = structured_profiler.invoke(system_prompt)
    
    # Format directly into dict for the state update mutation
    voice_blueprint = {
        "persona_title": guidelines_payload.persona_title,
        "tone_profile": guidelines_payload.tone_profile,
        "banned_phrases": guidelines_payload.banned_phrases,
        "narrative_hook_style": guidelines_payload.narrative_hook_style,
        "technical_density_rule": guidelines_payload.technical_density_rule
    }
    
    return {
        "voice_guidelines": voice_blueprint
    }