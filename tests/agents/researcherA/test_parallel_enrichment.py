import pytest
import json
from src.agents.researcherA.state import ResearcherALocalState
from src.agents.researcherA.graph import build_researcher_a_graph
from dotenv import load_dotenv

load_dotenv()


def test_full_researcher_a_pipeline_via_graph():
    """
    Real integration test: End-to-end ResearcherA pipeline using the compiled graph.
    Invokes: Radar → Dispatcher → Parallel Enrichment → Reducer → Voice → Strategy → End
    
    Tests all 4 nodes:
    1. integration_prob (Radar)
    2. enrichment workers (Parallel)
    3. voice_profiling_node (Voice)
    4. campaign_strategy_node (Strategy)
    
    Displays complete output for validation.
    """
    
    print("\n" + "="*80)
    print("🚀 RESEARCHER A PIPELINE TEST - USING COMPILED GRAPH")
    print("="*80)
    
    # Build the compiled graph
    graph = build_researcher_a_graph()
    
    # Prepare initial state
    initial_state: ResearcherALocalState = {
        "macro_trigger": "Serverless SaaS platform suffering frequent user churn and support tickets because API throttling and database connection pool exhaustion are causing intermittent service failures and slow customer onboarding.",
        "executed_queries": [],
        "raw_scraped_artifacts": [],
        "synthesized_trends": [],
        "selected_trend": None,
        "enriched_context": None,
        "enriched_trend_items": [],
        "enriched_trends": [],
        "voice_guidelines": None,
        "campaign_strategy": None
    }
    
    print("\n📥 INPUT STATE:")
    print(f"   Macro Trigger: {initial_state['macro_trigger']}")
    
    # ========== INVOKE THE COMPILED GRAPH ==========
    print("\n🔄 Invoking compiled graph...")
    print("   Pipeline: Radar → Dispatcher → [Parallel Workers] → Reducer → Voice → Strategy")
    
    try:
        final_state = graph.invoke(initial_state)
        print("✅ Graph execution completed")
    except Exception as e:
        print(f"❌ Graph execution failed: {str(e)}")
        raise
    
    # ========== VALIDATE & DISPLAY STAGE 1: RADAR OUTPUT ==========
    print("\n" + "-"*80)
    print("📊 STAGE 1: RADAR - Discovered Trends")
    print("-"*80)
    
    trends = final_state.get("synthesized_trends", [])
    print(f"   Total trends discovered: {len(trends)}")
    if len(trends) > 0:
        for i, trend in enumerate(trends[:5], 1):  # Show first 5
            print(f"\n   Trend {i}:")
            print(f"      Title: {trend.get('thematic_title', 'N/A')}")
            print(f"      Category: {trend.get('category', 'N/A')}")
            print(f"      Root Cause: {trend.get('underlying_cause', 'N/A')[:100]}...")
            print(f"      Business Impact: {trend.get('business_consequence', 'N/A')[:100]}...")
    
    # ========== VALIDATE & DISPLAY STAGE 2: ENRICHED TRENDS ==========
    print("\n" + "-"*80)
    print("📚 STAGE 2: ENRICHMENT - Parallel-Enriched Trends")
    print("-"*80)
    
    enriched_trends = final_state.get("enriched_trends")
    if enriched_trends:
        print(f"   Total enriched trends: {len(enriched_trends)}")
        for i, enriched in enumerate(enriched_trends[:3], 1):  # Show first 3
            context_len = len(enriched.get("enriched_context", ""))
            print(f"\n   Enriched Trend {i}:")
            print(f"      Title: {enriched['trend'].get('thematic_title', 'N/A')}")
            print(f"      Context Length: {context_len} chars")
            print(f"      Context Preview: {enriched.get('enriched_context', '')[:150]}...")
    else:
        print("   ⚠️ No enriched trends found")
    
    # ========== VALIDATE & DISPLAY STAGE 3: VOICE GUIDELINES ==========
    print("\n" + "-"*80)
    print("🎭 STAGE 3: VOICE - Persona Guidelines")
    print("-"*80)
    
    voice = final_state.get("voice_guidelines")
    if voice:
        print(f"\n   Persona Title: {voice.get('persona_title', 'N/A')}")
        print(f"\n   Tone Profile:")
        for tone in voice.get('tone_profile', []):
            print(f"      • {tone}")
        print(f"\n   Banned Phrases:")
        for phrase in voice.get('banned_phrases', [])[:5]:
            print(f"      • {phrase}")
        print(f"\n   Narrative Hook Style: {voice.get('narrative_hook_style', 'N/A')}")
        print(f"\n   Technical Density Rule: {voice.get('technical_density_rule', 'N/A')}")
    else:
        print("   ⚠️ No voice guidelines generated")
    
    # ========== VALIDATE & DISPLAY STAGE 4: CAMPAIGN STRATEGY ==========
    print("\n" + "-"*80)
    print("📋 STAGE 4: STRATEGY - Campaign Blueprint")
    print("-"*80)
    
    strategy = final_state.get("campaign_strategy")
    if strategy:
        print(f"\n   Master Campaign Angle:")
        print(f"      {strategy.get('master_campaign_angle', 'N/A')}")
        
        print(f"\n   Key Narrative Pillars:")
        for i, pillar in enumerate(strategy.get('key_narrative_pillars', []), 1):
            print(f"      {i}. {pillar}")
        
        print(f"\n   Platform Blueprints:")
        for platform, blueprint in strategy.get('platform_blueprints', {}).items():
            print(f"\n      [{platform}]")
            print(f"         Format: {blueprint.get('format_focus', 'N/A')}")
            print(f"         Core Argument: {blueprint.get('core_argument', 'N/A')[:100]}...")
    else:
        print("   ⚠️ No campaign strategy generated")
    
    # ========== FULL OUTPUT DUMP (JSON) ==========
    print("\n" + "="*80)
    print("📄 FULL STATE OUTPUT (JSON)")
    print("="*80)
    print(json.dumps({
        "trends_count": len(final_state.get("synthesized_trends", [])),
        "enriched_trends_count": len(final_state.get("enriched_trends", [])) if final_state.get("enriched_trends") else 0,
        "has_voice_guidelines": bool(final_state.get("voice_guidelines")),
        "has_campaign_strategy": bool(final_state.get("campaign_strategy")),
        "voice_guidelines": final_state.get("voice_guidelines"),
        "campaign_strategy": final_state.get("campaign_strategy")
    }, indent=2))
    
    # ========== ASSERTIONS ==========
    print("\n" + "="*80)
    print("✅ VALIDATION RESULTS")
    print("="*80)
    
    assert len(trends) > 0, "❌ Radar must discover at least 1 trend"
    print("✅ Radar discovered trends")
    
    assert enriched_trends and len(enriched_trends) > 0, "❌ Enrichment must produce enriched_trends"
    print(f"✅ Parallel enrichment produced {len(enriched_trends)} enriched trends")
    
    assert voice is not None, "❌ Voice node must generate guidelines"
    print("✅ Voice profiling node generated persona guidelines")
    
    assert strategy is not None, "❌ Strategy node must generate campaign blueprint"
    print("✅ Campaign strategy node generated blueprint")
    
    assert "master_campaign_angle" in strategy, "❌ Strategy missing master_campaign_angle"
    print("✅ Strategy has master_campaign_angle")
    
    assert "platform_blueprints" in strategy, "❌ Strategy missing platform_blueprints"
    print("✅ Strategy has platform_blueprints")
    
    print("\n" + "="*80)
    print("🎉 FULL PIPELINE TEST PASSED")
    print("="*80 + "\n")
    
    return final_state


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
