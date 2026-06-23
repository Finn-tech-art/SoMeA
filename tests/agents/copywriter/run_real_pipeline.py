import os
import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "src"
print('RUN_REAL_PIPELINE ROOT=', ROOT)
print('RUN_REAL_PIPELINE SRC=', SRC)
print('RUN_REAL_PIPELINE sys.path before insertion=', sys.path[:5])
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
print('RUN_REAL_PIPELINE sys.path after insertion=', sys.path[:5])

from src.agents.researcherA.graph import researcher_a_graph
from src.agents.copywriter.graph import copywriter_graph


def main():
    print("=== ENVIRONMENT ===")
    print("GROQ_API_KEY_1 set:", bool(os.getenv("GROQ_API_KEY_1")))
    print("=== RUNNING ResearcherA Graph ===")
    researcher_result = researcher_a_graph.invoke({"macro_trigger": "Kenyan etims integration into business systems 2026"})
    pprint(researcher_result)

    print("=== RUNNING Copywriter Graph ===")
    copywriter_result = copywriter_graph.invoke(researcher_result)
    pprint(copywriter_result)


if __name__ == '__main__':
    main()
