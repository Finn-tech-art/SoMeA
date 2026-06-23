import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class FacebookCopySchema(BaseModel):
    copy_facebook: str = Field(description="A Facebook post with a narrative arc and a persuasive CTA.")


def copy_facebook_node(state: CopywriterState) -> dict:
    brief = state.get("copy_brief", "")
    prompt = (
        "You are a social content writer for high-value enterprise audiences. "
        "Write a Facebook post that frames the problem, explains the app-enabled solution, "
        "and closes with a concise action prompt for decision makers. "
        "Keep the copy professional but relatable.\n\n"
        f"BRIEF:\n{brief}\n\n"
        "Return only a JSON object with the field `copy_facebook`."
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.34)
    structured = llm.with_structured_output(FacebookCopySchema)
    result = structured.invoke(prompt)
    return {"copy_facebook": result.copy_facebook}
