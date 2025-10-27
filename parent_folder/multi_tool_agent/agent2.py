# from google.adk.agents import Agent
# defining the basic identity, adding instructions, and defining tool functions
# dashboard_agent = Agent(
  #  model="gemini-2.0-flash",
   # name="dashboard_agent",
   # description="Answers user questions about what unique MBAN cohorts are doing",
   # instruction="""You are an agent that provides a summary of what unqiue MBAN (Master of Business Analytics) cohorts are currently doing professionally. 
   # When a user asks for information about a MBAN cohort:
   # 1.Identify the year of the cohort from the user's query.
   # 2. Use the 'get_info' tool to find the members who have shared their data with schulich.dotsnet.org/c/schulich/members
   # 3. Respond clearly to the user, writing a brief and concise summary that is no greater than five sentences, 
   # stating the year of the cohort, the employment rate of the cohort, the top five job titles, the top three industries, 
   # Example Query: "What's the MBAN cohort of {year} doing?"
   # Example Response: "The MBAN cohort of 2023 has 70 alumni. The most common job titles for this cohort are: Business Analyst (50%), Securities Analyst (17%), 
   # Investment Analyst (10%), Consultant (8%), Data Scientist (2.5%). The top industries where these alumni work are: Financials (70%), Pharmaceuticals (12%), 
   # and Telecommunications (5%). The 2023 alumni are predominately focused on networking opportunities and introductions to mid-career professionals who can provide mentorship 
   # and hiring referrals. A connection opportunity with an increased likelihood of a favourable outcome is Alexandr Wang MBAN '23 with Steve Ballmer, 
   # Director of Growth at Silicon Valley Bank."
   # """,
   # tools=[get_info]
#)
