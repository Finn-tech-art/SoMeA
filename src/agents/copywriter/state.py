from typing import TypedDict, Optional, List, Dict, Annotated
import operator

class VoiceGuidelines(TypedDict):
    persona_title: str
    tone_profile: List[str]
    banned_phrases: List[str]
    narrative_hook_style: str
    technical_density_rule: str

class PlatformBlueprint(TypedDict):
    format_focus: str
    core_argument: str

class CampaignStrategy(TypedDict):
    master_campaign_angle: str
    key_narrative_pillars: List[str]
    platform_blueprints: Dict[str, PlatformBlueprint]

class EnrichedTrend(TypedDict):
    trend: Dict[str, str]
    enriched_context: str

class CopywriterState(TypedDict):
    # ResearcherA inputs
    voice_guidelines: Optional[VoiceGuidelines]
    campaign_strategy: Optional[CampaignStrategy]
    enriched_trends: Optional[List[EnrichedTrend]]
    selected_trend: Optional[Dict[str, str]]
    enriched_context: Optional[str]

    # Intermediate copywriter outputs
    copy_brief: Optional[str]
    channel_copy: Optional[Dict[str, str]]

    # Final structured outputs for each platform
    copy_x: Optional[str]
    copy_linkedin: Optional[str]
    copy_insta: Optional[str]
    copy_tiktok: Optional[str]
    copy_facebook: Optional[str]

    # Optional list collector for parallel copy generation
    platform_outputs: Annotated[List[Dict[str, str]], operator.add]
