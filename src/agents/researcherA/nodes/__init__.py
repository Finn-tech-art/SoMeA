"""Three nodes:
1. Deep market research node - runs the duckduckgo-search query to scrape real time tech industry problems, trending engineering topics, and software founder complaints together with business complaints.
explicitly mines developer forums, industry articles, and B2B SaaS complaints.
2. architectural voice alignment - Your Qdrant Collection (team_voice) must be populated with points of view regarding your core service catalog (e.g., why 
custom middleware beats generic iPaaS, or the security benefit of your custom client portals). When Node 4 isolates a problem, Node 5 performs a semantic vector lookup to 
extract your specific solution thesis.
3. B2B strategy framing - Multi-key load balancer to execute deep analysis prompt.

"""