# Project Architecture

## Overview

This repository organizes its agent system under `src/agents/` as a package of distinct agent domains. Each agent domain is implemented as a subpackage containing:

- an `__init__.py` package entry point
- a `state.py` module for agent-specific state models or state handling
- a `nodes/` subpackage containing functional node modules

The structure suggests a modular, pipeline-oriented architecture where specialized agents collaborate through clearly separated responsibilities.

## Agent packages

### `src/agents/coordinator`
- Purpose: orchestration, routing, and human-in-the-loop validation.
- Key files:
  - `__init__.py` — coordinator description and package entry point
  - `state.py` — coordinator state model placeholder
  - `nodes/`:
    - `hil.py` — human-in-the-loop workflow
    - `market_intel.py` — market intelligence or research coordination
    - `routing.py` — routing and task distribution logic

### `src/agents/researcherA`
- Purpose: strategy and research support.
- Key files:
  - `__init__.py`
  - `state.py`
  - `nodes/`:
    - `voice.py` — voice/personality guidance
    - `strategy.py` — strategy generation or planning
    - `integration_prob.py` — integration problem analysis

### `src/agents/researcherB`
- Purpose: trend/idea research and concept development.
- Key files:
  - `__init__.py`
  - `state.py`
  - `nodes/`:
    - `tech_culture.py` — technology and culture research
    - `meme_to_product.py` — trend-to-product ideas
    - `ideation.py` — ideation or brainstorming

### `src/agents/copywriter`
- Purpose: messaging and social copy generation.
- Key files:
  - `__init__.py`
  - `state.py`
  - `nodes/`:
    - `x.py`
    - `tiktok.py`
    - `linkedin.py`
    - `insta.py`
    - `facebook.py`

### `src/agents/media`
- Purpose: media creation, scraping, and content assembly.
- Key files:
  - `__init__.py`
  - `state.py`
  - `nodes/`:
    - `pinterest_crawler.py` — visual research / inspiration scraping
    - `moviepy.py` — video or clip generation
    - `meme.py` — meme creation or formatting
    - `harvester.py` — content harvesting / aggregation
    - `caurosel.py` — carousel graphics or multi-frame media

### `src/agents/broadcaster`
- Purpose: distribution and analytics.
- Key files:
  - `__init__.py`
  - `state.py`
  - `nodes/`:
    - `sync.py` — synchronization or publishing orchestration
    - `broadcast.py` — content distribution
    - `analytics.py` — performance measurement or analytics

## Architectural pattern

The repository follows a domain-driven agent architecture:

- Each agent domain is isolated in its own package.
- `state.py` is reserved for agent-local state and runtime context.
- `nodes/` contains actionable components or nodes, likely representing discrete graph/step operations.
- The coordinator agent sits at the top layer to route work, validate results, and manage flow between specialist agents.
- Researchers produce insights and strategy.
- Copywriter turns ideas into platform-specific messaging.
- Media generates and prepares rich assets.
- Broadcaster publishes and tracks performance.

## Inferred data flow

1. `researcherA` / `researcherB` produce insights, strategy, and campaign ideas.
2. `coordinator` validates, routes, and decides what should move next.
3. `copywriter` generates social media text for each channel.
4. `media` creates visuals, videos, memes, and content assets.
5. `broadcaster` synchronizes distribution and collects analytics.

## Notes

- The top-level `src/agents/__init__.py` and `src/agents/state.py` are currently empty, indicating package setup without global implementation yet.
- `architecture.md` is based on the current package layout and naming conventions.
- If more detailed implementation exists elsewhere in the repo, the architecture can be refined using actual data flow and imports.
