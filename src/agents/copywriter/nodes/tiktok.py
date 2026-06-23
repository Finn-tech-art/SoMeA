import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class TikTokCopySchema(BaseModel):
    copy_tiktok: str = Field(description="A TikTok video script or short-form caption for product storytelling.")


def copy_tiktok_node(state: CopywriterState) -> dict:
    brief = state.get("copy_brief", "")
    prompt = (
        "You are a short-form video scriptwriter for enterprise app marketing. "
        "Write a TikTok-style script outline with a hook, three action beats, and one strong ending CTA. "
        "Keep it dynamic, visual, and simple enough for a video creator to produce.\n\n"
        f"BRIEF:\n{brief}\n\n"
        "Return only a JSON object with the field `copy_tiktok`."
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.38)
    structured = llm.with_structured_output(TikTokCopySchema)
    result = structured.invoke(prompt)
    return {"copy_tiktok": result.copy_tiktok}
