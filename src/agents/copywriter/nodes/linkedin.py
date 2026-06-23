import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class LinkedInCopySchema(BaseModel):
    copy_linkedin: str = Field(description="A LinkedIn post or carousel script with narrative structure.")


def copy_linkedin_node(state: CopywriterState) -> dict:
    brief = state.get("copy_brief", "")
    strategy = state.get("campaign_strategy", {})
    prompt = (
        "You are a senior LinkedIn content strategist for enterprise apps. "
        "Create a LinkedIn post that reads like a single cohesive article or carousel narrative, "
        "using the campaign angle, key narrative pillars, and target audience. "
        "Include a strong opening, a few supporting paragraphs or slides, and a final call to action.\n\n"
        f"CAMPAIGN ANGLE: {strategy.get('master_campaign_angle', '')}\n"
        f"NARRATIVE PILLARS: {', '.join(strategy.get('key_narrative_pillars', []))}\n"
        f"PLATFORMS: {', '.join(strategy.get('platform_blueprints', {}).keys())}\n\n"
        f"BRIEF:\n{brief}\n\n"
        "Return only a JSON object with the field `copy_linkedin`."
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.33)
    structured = llm.with_structured_output(LinkedInCopySchema)
    result = structured.invoke(prompt)
    return {"copy_linkedin": result.copy_linkedin}
