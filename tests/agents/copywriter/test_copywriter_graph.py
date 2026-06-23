from types import SimpleNamespace

from src.agents.copywriter.graph import build_copywriter_graph, copywriter_graph
from src.agents.copywriter.nodes.copybrief import ChatGroq, CopyBriefSchema, copy_brief_node
from src.agents.copywriter.nodes.x import XCopySchema
from src.agents.copywriter.nodes.linkedin import LinkedInCopySchema
from src.agents.copywriter.nodes.insta import InstaCopySchema
from src.agents.copywriter.nodes.tiktok import TikTokCopySchema
from src.agents.copywriter.nodes.facebook import FacebookCopySchema
from src.agents.researcherA.graph import researcher_a_graph
from src.agents.researcherA.nodes.integration_prob import QueryMatrixSchema, DiscoverySynthesisSchema
from src.agents.researcherA.nodes.strategy import CampaignStrategySchema
from src.agents.researcherA.nodes.voice import VoiceGuardrailsSchema


class FakeStructuredOutput:
    def __init__(self, schema):
        self.schema = schema

    def invoke(self, prompt: str):
        name = self.schema.__name__
        if name == "QueryMatrixSchema":
            return SimpleNamespace(
                developer_query="developer forum query",
                founder_query="founder hub query",
                b2b_complaint_query="b2b complaint query",
            )
        if name == "DiscoverySynthesisSchema":
            return SimpleNamespace(
                discovered_trends=[
                    SimpleNamespace(
                        category="Technical Architecture",
                        thematic_title="Database starvation",
                        underlying_cause="Connection pool exhaustion",
                        business_consequence="Slow response times and customer churn",
                    )
                ]
            )
        if name == "VoiceGuardrailsSchema":
            return SimpleNamespace(
                persona_title="Skeptical CTO",
                tone_profile=["direct", "specific"],
                banned_phrases=["revolutionize", "game-changing"],
                narrative_hook_style="Open with a painful engineering failure",
                technical_density_rule="Be clear and concise for technical readers",
            )
        if name == "CampaignStrategySchema":
            return SimpleNamespace(
                master_campaign_angle="Align engineering resilience with business velocity",
                key_narrative_pillars=["trust", "speed", "clarity"],
                platform_blueprints={
                    "linkedin": SimpleNamespace(format_focus="carousel", core_argument="build trust through transparency"),
                    "x": SimpleNamespace(format_focus="thread", core_argument="share rapid debugging insights"),
                    "instagram": SimpleNamespace(format_focus="story", core_argument="visualize team wins"),
                },
            )
        if name == "CopyBriefSchema":
            return SimpleNamespace(
                copy_brief="A compelling campaign brief.",
                recommended_tone="trustworthy",
                focus_audience="engineering leaders",
                creative_hook="Stop losing time to integration outages",
            )
        if name == "XCopySchema":
            return SimpleNamespace(copy_x="X thread copy.")
        if name == "LinkedInCopySchema":
            return SimpleNamespace(copy_linkedin="LinkedIn copy.")
        if name == "InstaCopySchema":
            return SimpleNamespace(copy_insta="Instagram copy.")
        if name == "TikTokCopySchema":
            return SimpleNamespace(copy_tiktok="TikTok copy.")
        if name == "FacebookCopySchema":
            return SimpleNamespace(copy_facebook="Facebook copy.")
        return SimpleNamespace(content="Fallback content")


class FakeChatGroq:
    def __init__(self, model: str, api_key: str, temperature: float):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature

    def with_structured_output(self, schema, **kwargs):
        return FakeStructuredOutput(schema)

    def invoke(self, prompt: str):
        return SimpleNamespace(content="Fallback content for direct LLM invocation.")


def test_copy_brief_node_returns_structured_copy_brief(monkeypatch):
    monkeypatch.setattr("src.agents.copywriter.nodes.copybrief.ChatGroq", FakeChatGroq)

    fake_state = {
        "voice_guidelines": {
            "persona_title": "Growth Marketing Leader",
            "tone_profile": ["clear", "authoritative"],
            "banned_phrases": ["best in class", "game changer"],
            "narrative_hook_style": "Customer pain first",
            "technical_density_rule": "Keep it accessible",
        },
        "campaign_strategy": {
            "master_campaign_angle": "Make decision-making faster for distributed teams",
            "key_narrative_pillars": ["speed", "trust", "insights"],
            "platform_blueprints": {
                "linkedin": {"format_focus": "carousel", "core_argument": "data-driven decisions"},
            },
        },
        "enriched_trends": [
            {
                "trend": {
                    "thematic_title": "Real-time collaboration",
                    "category": "Productivity",
                    "business_consequence": "Teams need faster consensus without meetings.",
                },
                "enriched_context": "This trend shows how distributed work makes real-time sync a competitive advantage.",
            }
        ],
        "selected_trend": {
            "thematic_title": "Real-time collaboration",
        },
        "enriched_context": "A concise context summary for the selected trend.",
    }

    result = copy_brief_node(fake_state)

    assert result["copy_brief"] == "A compelling campaign brief."
    assert result["platform_outputs"][0]["platform"] == "generic"
    assert result["platform_outputs"][0]["recommended_tone"] == "trustworthy"
    assert result["platform_outputs"][0]["focus_audience"] == "engineering leaders"
    assert result["platform_outputs"][0]["creative_hook"] == "Stop losing time to integration outages"


def test_copywriter_graph_compiles_and_contains_expected_nodes():
    compiled = copywriter_graph
    assert compiled.input_channels == "__start__"
    assert "copy_brief" in compiled.nodes
    assert "copy_x" in compiled.nodes
    assert "copy_linkedin" in compiled.nodes
    assert "copy_insta" in compiled.nodes
    assert "copy_tiktok" in compiled.nodes
    assert "copy_facebook" in compiled.nodes

    expected_outputs = {
        "copy_brief",
        "copy_x",
        "copy_linkedin",
        "copy_insta",
        "copy_tiktok",
        "copy_facebook",
        "platform_outputs",
    }
    assert expected_outputs.issubset(set(compiled.output_channels))

    second_compiled = build_copywriter_graph()
    assert type(second_compiled) == type(compiled)
    assert second_compiled.output_channels == compiled.output_channels


def test_x_copy_node_handles_list_structured_outputs(monkeypatch):
    from src.agents.copywriter.nodes.x import _extract_copy_x

    fake_result = {
        "parsed": {"copy_x": [
            "1/4: Hook on integration failure.",
            "2/4: Explain pain and solution.",
            "3/4: Provide value bullets.",
            "4/4: Strong CTA."
        ]},
        "raw": None,
        "parsing_error": None,
    }

    assert _extract_copy_x(fake_result) == (
        "1/4: Hook on integration failure.\n"
        "2/4: Explain pain and solution.\n"
        "3/4: Provide value bullets.\n"
        "4/4: Strong CTA."
    )


def test_researcherA_to_copywriter_pipeline_integration(monkeypatch):
    def fake_jina_reader_fetch(url: str, timeout: int = 15) -> str:
        return "Mock reference content " * 20

    class FakeSearchWrapper:
        def __init__(self, max_results=None):
            self.max_results = max_results

        def results(self, query, max_results=None):
            return [
                {
                    "title": "Mock engineering post",
                    "link": "https://example.com/mock-article",
                    "snippet": "This is a mock snippet of engineering research.",
                }
            ]

    monkeypatch.setattr("src.agents.researcherA.nodes.integration_prob.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.researcherA.nodes.enrichment.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.researcherA.nodes.voice.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.researcherA.nodes.strategy.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.copybrief.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.x.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.linkedin.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.insta.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.tiktok.ChatGroq", FakeChatGroq)
    monkeypatch.setattr("src.agents.copywriter.nodes.facebook.ChatGroq", FakeChatGroq)

    monkeypatch.setattr(
        "src.agents.researcherA.nodes.integration_prob.DuckDuckGoSearchAPIWrapper",
        FakeSearchWrapper,
    )
    monkeypatch.setattr(
        "src.agents.researcherA.nodes.enrichment.DuckDuckGoSearchAPIWrapper",
        FakeSearchWrapper,
    )
    monkeypatch.setattr(
        "src.agents.researcherA.nodes.enrichment.jina_reader_fetch",
        fake_jina_reader_fetch,
    )

    researcher_state = researcher_a_graph.invoke({"macro_trigger": "SaaS incident response delays 2026"})

    assert researcher_state["selected_trend"]["thematic_title"] == "Database starvation"
    assert researcher_state["voice_guidelines"]["persona_title"] == "Skeptical CTO"
    assert researcher_state["campaign_strategy"]["master_campaign_angle"] == "Align engineering resilience with business velocity"

    copywriter_result = copywriter_graph.invoke(researcher_state)
    assert copywriter_result["copy_brief"] == "A compelling campaign brief."
    assert copywriter_result["copy_x"] == "X thread copy."
    assert copywriter_result["copy_linkedin"] == "LinkedIn copy."
    assert copywriter_result["copy_insta"] == "Instagram copy."
    assert copywriter_result["copy_tiktok"] == "TikTok copy."
    assert copywriter_result["copy_facebook"] == "Facebook copy."
