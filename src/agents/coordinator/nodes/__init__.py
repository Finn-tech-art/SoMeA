"""The three nodes for the coordinator agent:
1. Market intelligence node - calculates current time offsets across target tech hubs
using pytz to determine the single best upcoming B2B angagement hour.
2. Human in the loop Gateway node - Syncs with the streamlit UI and supabase, pausing the entire
stategraph until the team manually reviews the content.
3. Conditional routing node - Evaluates the human review response. If approved Y it passes the state to the publisher
, if rejected it captures your textual feedback and channels the state back to the strategy node for rewrites.

"""