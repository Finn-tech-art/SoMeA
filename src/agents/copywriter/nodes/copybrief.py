import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class CopyBriefSchema(BaseModel):
    copy_brief: str = Field(description="A concise creative brief summarizing the campaign direction.")
    recommended_tone: str = Field(description="The most suitable tone and style for the campaign.")
    focus_audience: str = Field(description="The primary customer or business audience this campaign should speak to.")
    creative_hook: str = Field(description="The leading hook or headline concept for the campaign.")


def copy_brief_node(state: CopywriterState) -> dict:
    """Generates a campaign copy brief from researcher output and voice strategy."""
    voice = state.get("voice_guidelines") or {}
    strategy = state.get("campaign_strategy") or {}
    enriched_trends = state.get("enriched_trends") or []
    selected_trend = state.get("selected_trend") or {}
    enriched_context = state.get("enriched_context") or ""

    # Build the prompt from the researcher output
    voice_description = (
        f"Persona: {voice.get('persona_title', 'N/A')}\n"
        f"Tone directives: {', '.join(voice.get('tone_profile', []))}\n"
        f"Banned phrases: {', '.join(voice.get('banned_phrases', []))}\n"
        f"Hook style: {voice.get('narrative_hook_style', 'N/A')}\n"
        f"Density rule: {voice.get('technical_density_rule', 'N/A')}\n"
    )

    strategy_description = (
        f"Campaign angle: {strategy.get('master_campaign_angle', 'N/A')}\n"
        f"Key pillars: {', '.join(strategy.get('key_narrative_pillars', []))}\n"
        f"Platforms: {', '.join(strategy.get('platform_blueprints', {}).keys())}\n"
    )

    trend_description = "".join(
        f"- {trend['trend'].get('thematic_title', 'N/A')} ({trend['trend'].get('category', 'N/A')}): {trend['trend'].get('business_consequence', '')}\n"
        for trend in enriched_trends[:3]
    )

    primary_trend = selected_trend.get('thematic_title', 'N/A')
    primary_context = enriched_context[:3000]

    prompt = (
        "You are a high-performing B2B copy strategist. Use the researcher output below to create a campaign brief "
        "that is app-focused, customer-centric, and ready for downstream social copywriting. "
        "Include the target audience, recommended tone, and a headline hook.\n\n"
        "VOICE GUIDELINES:\n"
        f"{voice_description}\n"
        "CAMPAIGN STRATEGY:\n"
        f"{strategy_description}\n"
        "TOP TRENDS:\n"
        f"{trend_description}\n"
        "PRIMARY TREND:\n"
        f"{primary_trend}\n"
        "PRIMARY CONTEXT:\n"
        f"{primary_context}\n"
        "\nRespond with a structured creative brief in JSON format matching the schema."        
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY_1"),
        temperature=0.3,
    )
    structured = llm.with_structured_output(CopyBriefSchema)
    brief_payload = structured.invoke(prompt)

    return {
        "copy_brief": brief_payload.copy_brief,
        "platform_outputs": [
            {
                "platform": "generic",
                "recommended_tone": brief_payload.recommended_tone,
                "focus_audience": brief_payload.focus_audience,
                "creative_hook": brief_payload.creative_hook,
            }
        ]
    }
