import json
import os
import re
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from src.agents.copywriter.state import CopywriterState

load_dotenv()


class XCopySchema(BaseModel):
    copy_x: str | list[str] = Field(description="A compact X thread or tweet sequence optimized for engagement.")


def _parse_json_output(raw_output: str) -> dict | None:
    if not isinstance(raw_output, str):
        return None

    normalized = raw_output.strip()
    normalized = re.sub(r"^```(?:json)?\s*", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s*```$", "", normalized, flags=re.IGNORECASE)

    match = re.search(r"\{.*\}", normalized, flags=re.DOTALL)
    if not match:
        return None

    candidate = match.group(0)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        # Fallback for malformed JSON that still contains a copy_x field.
        key_match = re.search(
            r'"copy_x"\s*:\s*"(.*?)"\s*(?:,|})',
            candidate,
            flags=re.DOTALL,
        )
        if key_match:
            return {"copy_x": key_match.group(1)}
        return None


def _extract_copy_x(output) -> str | None:
    if output is None:
        return None

    if isinstance(output, dict):
        if "parsed" in output or "raw" in output or "parsing_error" in output:
            parsed = output.get("parsed")
            if parsed is not None:
                return _extract_copy_x(parsed)
            raw = output.get("raw")
            if raw is not None:
                raw_text = getattr(raw, "content", None) if not isinstance(raw, dict) else raw.get("content")
                return _extract_copy_x(raw_text)

        if "copy_x" in output:
            return _extract_copy_x(output["copy_x"])
        return None

    if hasattr(output, "copy_x"):
        return _extract_copy_x(output.copy_x)

    if isinstance(output, list):
        return "\n".join(str(item) for item in output)

    if isinstance(output, str):
        parsed = _parse_json_output(output)
        if parsed and "copy_x" in parsed:
            return _extract_copy_x(parsed["copy_x"])
        return output

    return None


def copy_x_node(state: CopywriterState) -> dict:
    brief = state.get("copy_brief", "")
    voice = state.get("voice_guidelines", {})
    prompt = (
        "You are a high-performing B2B social copywriter specialized in X (formerly Twitter). "
        "Write a concise X thread that opens with a strong hook, presents 3 value-packed points, "
        "and finishes with a compelling call to action for app-driven decision makers. "
        "Use the brand voice and campaign angle below.\n\n"
        f"VOICE: {voice.get('persona_title', 'Professional Analyst')}\n"
        f"TONE: {', '.join(voice.get('tone_profile', []))}\n"
        f"BANNED PHRASES: {', '.join(voice.get('banned_phrases', []))}\n"
        f"HOOK STYLE: {voice.get('narrative_hook_style', 'Direct problem statement.')}\n"
        f"DENSITY: {voice.get('technical_density_rule', 'Maintain basic text clarity.')}\n\n"
        f"CAMPAIGN BRIEF:\n{brief}\n\n"
        "Return only a single JSON object with the field `copy_x`. "
        "Do not wrap the output in markdown fences."
    )

    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY_1"), temperature=0.35)
    structured = llm.with_structured_output(XCopySchema, method="json_mode", include_raw=True)
    result = None
    try:
        result = structured.invoke(prompt)
    except Exception:
        result = None

    extracted = _extract_copy_x(result)
    if extracted is not None:
        return {"copy_x": extracted}

    raw = llm.invoke(prompt)
    raw_text = getattr(raw, "content", None)
    extracted = _extract_copy_x(raw_text)
    if extracted is not None:
        return {"copy_x": extracted}

    return {"copy_x": str(raw_text if raw_text is not None else raw)}
