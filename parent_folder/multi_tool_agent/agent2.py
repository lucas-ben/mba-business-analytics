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

from google.adk.agents import Agent
import json
from typing import Dict, List, Optional

# Define your tool function FIRST
def get_info(year: int) -> dict:
    """
    Retrieves information about MBAN cohort members for a specific year.
    
    Args:
        year (int): The graduation year of the MBAN cohort
        
    Returns:
        dict: Information about the cohort including employment stats, job titles, and industries
    """
    
    # Mock data for now - you'll replace this with actual data retrieval
    # from schulich.dotsnet.org/c/schulich/members or your data source
    
    mock_data = {
        2023: {
            "total_alumni": 70,
            "employment_rate": 92,
            "job_titles": {
                "Business Analyst": 50,
                "Securities Analyst": 17,
                "Investment Analyst": 10,
                "Consultant": 8,
                "Data Scientist": 2.5
            },
            "industries": {
                "Financials": 70,
                "Pharmaceuticals": 12,
                "Telecommunications": 5
            },
            "trending_topics": [
                "networking opportunities",
                "mentorship seeking",
                "career transitions to tech"
            ],
            "connection_opportunities": [
                {
                    "alumni": "Alexandr Wang MBAN '23",
                    "connection": "Steve Ballmer, Director of Growth at Silicon Valley Bank",
                    "reason": "hiring referrals in fintech"
                }
            ]
        },
        2024: {
            "total_alumni": 85,
            "employment_rate": 88,
            "job_titles": {
                "Data Analyst": 45,
                "Business Intelligence Analyst": 20,
                "Product Analyst": 15,
                "Consultant": 10,
                "Risk Analyst": 5
            },
            "industries": {
                "Technology": 55,
                "Financial Services": 25,
                "Consulting": 10
            },
            "trending_topics": [
                "AI/ML applications",
                "product management transitions",
                "startup opportunities"
            ],
            "connection_opportunities": [
                {
                    "alumni": "Sarah Chen MBAN '24",
                    "connection": "Jennifer Liu, VP Analytics at Shopify",
                    "reason": "analytics leadership opportunities"
                }
            ]
        }
    }
    
    # Check if we have data for the requested year
    if year in mock_data:
        return {
            "status": "success",
            "data": mock_data[year]
        }
    else:
        return {
            "status": "error",
            "message": f"No data available for MBAN cohort of {year}. Available years: {list(mock_data.keys())}"
        }

# Now define your agent with the tool
root_agent = Agent(  # Changed to 'root_agent' - REQUIRED name
    model="gemini-2.0-flash",
    name="dashboard_agent",
    description="Answers user questions about what unique MBAN cohorts are doing professionally",
    instruction="""You are an agent that provides a summary of what unique MBAN (Master of Business Analytics) cohorts are currently doing professionally. 
    
    When a user asks for information about a MBAN cohort:
    1. Identify the year of the cohort from the user's query
    2. Use the 'get_info' tool to retrieve cohort data
    3. Respond clearly with a brief and concise summary (no more than five sentences)
    
    Include in your response:
    - Year of the cohort and total number of alumni
    - Employment rate
    - Top 5 job titles with percentages
    - Top 3 industries with percentages
    - Trending topics among the cohort
    - Potential connection opportunities
    
    Format your response professionally and make it easy to scan.
    
    If data is not available for the requested year, inform the user politely and mention which years are available.""",
    tools=[get_info]  # Now this references the function defined above
)