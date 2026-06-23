import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class InstaCopySchema(BaseModel):
    copy_insta: str = Field(description="An Instagram caption with hook, body, CTA, and hashtags.")


def copy_insta_node(state: CopywriterState) -> dict:
    brief = state.get("copy_brief", "")
    voice = state.get("voice_guidelines", {})
    prompt = (
        "You are an Instagram copywriter for app-focused B2B brands. "
        "Write an Instagram caption that opens with a compelling hook, explains the problem and solution, "
        "and closes with a soft call to action. Include 4-5 relevant hashtags.\n\n"
        f"TONE: {', '.join(voice.get('tone_profile', []))}\n"
        f"HOOK STYLE: {voice.get('narrative_hook_style', '')}\n"
        f"DENSITY: {voice.get('technical_density_rule', '')}\n\n"
        f"BRIEF:\n{brief}\n\n"
        "Return only a JSON object with the field `copy_insta`."
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.32)
    structured = llm.with_structured_output(InstaCopySchema)
    result = structured.invoke(prompt)
    return {"copy_insta": result.copy_insta}
