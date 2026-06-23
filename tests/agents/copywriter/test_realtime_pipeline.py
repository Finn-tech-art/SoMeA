import json
import sys
import types
from pprint import pprint

# Stub optional external dependencies before importing ResearcherA modules.
if "langchain_community" not in sys.modules:
    langchain_community = types.ModuleType("langchain_community")
    utilities = types.ModuleType("langchain_community.utilities")

    class DuckDuckGoSearchAPIWrapper:
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

    utilities.DuckDuckGoSearchAPIWrapper = DuckDuckGoSearchAPIWrapper
    langchain_community.utilities = utilities
    sys.modules["langchain_community"] = langchain_community
    sys.modules["langchain_community.utilities"] = utilities

from src.agents.researcherA.graph import researcher_a_graph
from src.agents.copywriter.graph import copywriter_graph
import src.agents.researcherA.nodes.integration_prob as integration_prob
import src.agents.researcherA.nodes.enrichment as enrichment
import src.agents.researcherA.nodes.voice as voice
import src.agents.researcherA.nodes.strategy as strategy
import src.agents.copywriter.nodes.copybrief as copybrief
import src.agents.copywriter.nodes.x as x_node
import src.agents.copywriter.nodes.linkedin as linkedin_node
import src.agents.copywriter.nodes.insta as insta_node
import src.agents.copywriter.nodes.tiktok as tiktok_node
import src.agents.copywriter.nodes.facebook as facebook_node


def ensure_realtime_patching():
    class FakeStructuredOutput:
        def __init__(self, schema):
            self.schema = schema

        def invoke(self, prompt: str):
            name = self.schema.__name__
            if name == "QueryMatrixSchema":
                return types.SimpleNamespace(
                    developer_query="developer forum query",
                    founder_query="founder hub query",
                    b2b_complaint_query="b2b complaint query",
                )
            if name == "DiscoverySynthesisSchema":
                return types.SimpleNamespace(
                    discovered_trends=[
                        types.SimpleNamespace(
                            category="Technical Architecture",
                            thematic_title="Database starvation",
                            underlying_cause="Connection pool exhaustion",
                            business_consequence="Slow response times and customer churn",
                        )
                    ]
                )
            if name == "VoiceGuardrailsSchema":
                return types.SimpleNamespace(
                    persona_title="Skeptical CTO",
                    tone_profile=["direct", "specific"],
                    banned_phrases=["revolutionize", "game-changing"],
                    narrative_hook_style="Open with a painful engineering failure",
                    technical_density_rule="Be clear and concise for technical readers",
                )
            if name == "CampaignStrategySchema":
                return types.SimpleNamespace(
                    master_campaign_angle="Align engineering resilience with business velocity",
                    key_narrative_pillars=["trust", "speed", "clarity"],
                    platform_blueprints={
                        "linkedin": types.SimpleNamespace(format_focus="carousel", core_argument="build trust through transparency"),
                        "x": types.SimpleNamespace(format_focus="thread", core_argument="share rapid debugging insights"),
                        "instagram": types.SimpleNamespace(format_focus="story", core_argument="visualize team wins"),
                    },
                )
            if name == "CopyBriefSchema":
                return types.SimpleNamespace(
                    copy_brief="A compelling campaign brief.",
                    recommended_tone="trustworthy",
                    focus_audience="engineering leaders",
                    creative_hook="Stop losing time to integration outages",
                )
            if name == "XCopySchema":
                return types.SimpleNamespace(copy_x="X thread copy.")
            if name == "LinkedInCopySchema":
                return types.SimpleNamespace(copy_linkedin="LinkedIn copy.")
            if name == "InstaCopySchema":
                return types.SimpleNamespace(copy_insta="Instagram copy.")
            if name == "TikTokCopySchema":
                return types.SimpleNamespace(copy_tiktok="TikTok copy.")
            if name == "FacebookCopySchema":
                return types.SimpleNamespace(copy_facebook="Facebook copy.")
            return types.SimpleNamespace(content="Fallback content")

    class FakeChatGroq:
        def __init__(self, model: str, api_key: str, temperature: float):
            self.model = model
            self.api_key = api_key
            self.temperature = temperature

        def with_structured_output(self, schema, **kwargs):
            return FakeStructuredOutput(schema)

        def invoke(self, prompt: str):
            return types.SimpleNamespace(content="Fallback content for direct LLM invocation.")

    integration_prob.ChatGroq = FakeChatGroq
    enrichment.ChatGroq = FakeChatGroq
    voice.ChatGroq = FakeChatGroq
    strategy.ChatGroq = FakeChatGroq
    copybrief.ChatGroq = FakeChatGroq
    x_node.ChatGroq = FakeChatGroq
    linkedin_node.ChatGroq = FakeChatGroq
    insta_node.ChatGroq = FakeChatGroq
    tiktok_node.ChatGroq = FakeChatGroq
    facebook_node.ChatGroq = FakeChatGroq

    enrichment.jina_reader_fetch = lambda url, timeout=15: "Mock technical content for " + url


def test_realtime_pipeline():
    ensure_realtime_patching()

    print("\n=== Running ResearcherA Graph ===")
    researcher_result = researcher_a_graph.invoke({"macro_trigger": "SaaS incident response delays 2026"})
    pprint(researcher_result)

    print("\n=== Running Copywriter Graph ===")
    copywriter_result = copywriter_graph.invoke(researcher_result)
    pprint(copywriter_result)

    assert "copy_brief" in copywriter_result
    assert "copy_x" in copywriter_result
    assert "copy_linkedin" in copywriter_result
    assert "copy_insta" in copywriter_result
    assert "copy_tiktok" in copywriter_result
    assert "copy_facebook" in copywriter_result
