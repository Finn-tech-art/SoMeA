# SoMeA (Social Media Agent)

**SoMeA** is an enterprise-grade, multi-agent AI system built using **LangGraph** and **Groq** (powered by ultra-fast models like Llama 3). Moving far beyond simple, single-prompt corporate marketing bots, SoMeA models real human content creation workflows. It acts as an autonomous technical researcher, a brand strategist, and a native multi-platform copywriter.

The core engineering objective of SoMeA is to eliminate generic "AI fluff" (such as phrases like *"delve"*, *"revolutionize"*, or *"testament"*) by fueling downstream copywriters with high-density architectural facts, deep technical post-mortems, and strict, human-derived stylistic guardrails.

---

## Technical Stack
Orchestration: LangGraph (for complex stateful, multi-agent network topologies)

Inference Engine: ChatGroq API (llama-3.3-70b-versatile for structured reasoning, llama-3.1-8b-fast for fast transformations)

Structured Parsing: Pydantic v2 (forcing LLM outputs directly into predictable JSON/Python schemas)

Testing Framework: Pytest