from google.adk.agents import Agent

# defining the basic identity
dashboard_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="dashboard_agent",
    description="Answers users questions about what the MBAN cohort of 2026 is doing"
)