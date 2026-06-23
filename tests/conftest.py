import os
import sys
import types

# Ensure the src package root is available for pytest imports.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Provide lightweight stubs for optional external dependencies used by ResearcherA nodes during tests.
if "langchain_community" not in sys.modules:
    langchain_community = types.ModuleType("langchain_community")
    utilities = types.ModuleType("langchain_community.utilities")

    class DuckDuckGoSearchAPIWrapper:
        def __init__(self, max_results=None):
            self.max_results = max_results

        def results(self, query, max_results=None):
            return []

    utilities.DuckDuckGoSearchAPIWrapper = DuckDuckGoSearchAPIWrapper
    langchain_community.utilities = utilities
    sys.modules["langchain_community"] = langchain_community
    sys.modules["langchain_community.utilities"] = utilities
