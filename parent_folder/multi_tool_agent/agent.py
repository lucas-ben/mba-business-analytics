from google.adk.agents import Agent
import json
from typing import Dict, List, Optional
from collections import Counter
from datetime import datetime

# defining the basic identity, adding instructions, and defining tool functions

def get_info(year: int) -> dict:
    """
    Retrieves information about MBAN cohort members for a specific year.
    
    Args:
        year (int): The graduation year of the MBAN cohort 
        
    Returns:
        dict: Information about the cohort including member details, skills, and networking
    """
    # helper function to normalize city location 
    def normalize_city(location: str) -> str:
        if not location:
            return "NaN"

        location = location.lower()

        city_map = {
            "toronto": "Toronto",
            "greater toronto area": "Toronto",
            "gta": "Toronto",
            "kitchener": "Kitchener",
            "waterloo": "Waterloo",
            "mississauga": "Mississauga",
            "vancouver": "Vancouver"
        }

        for keyword, city in city_map.items():
            if keyword in location:
                return city

        return "Canada" if "canada" in location else "NaN"
    
    # example dataset 
    members_database = {
        2026: [  
            {
                "name": "Lucas Ben",
                "joined": "10/12/2025",
                "title": "Business Analytics Graduate Student",
                "location": "Toronto, ON",
                "linkedin": "https://linkedin.com/in/LinkedIn",
                "description": "Business analytics graduate student with expertise in translating complex business problems into data-driven analytical solutions. Experienced in machine learning, AI system development, and statistical inference.",
                "skills": ["Machine Learning", "Bayesian Modeling", "NLP", "AI Development", "Statistical Inference", 
                          "Data Pipelines", "ETL Architecture", "API Integration", "Sensitivity Analysis", 
                          "Python", "SQL", "Julia", "R", "HTML/CSS", "PyMC"],
                "offers": ["NaN"],
                 "asks": ["NaN"]
            },
            {
                "name": "Hasti Bagherzadi",
                "joined": "10/3/2025",
                "title": "MBAN Candidate - AI & Machine Learning Focus",
                "location": "Canada",
                "linkedin": "https://linkedin.com/in/hastibgh",
                "description": "MBAN 26' @ Schulich School of Business. Passionate about the intersection of data, technology, and strategy. Focus on AI agents and automation.",
                "skills": ["SQL", "Problem Solving", "Machine Learning", "Business Analytics", 
                          "AI & Machine Learning", "AI Agents & Automation"],
                "offers": ["NaN"],
                "asks": ["NaN"],
            },
            {
                "name": "Aisha Ibrahim",
                "joined": "10/2/2025",
                "title": "Business & Data Analyst",
                "location": "Kitchener, Ontario, Canada",
                "linkedin": "https://www.linkedin.com/in/aisha-ibrahim-427258160",
                "description": "Business Analyst and Project Coordinator with over 4 years of experience. Strong foundation in data-driven decision-making, project execution, and stakeholder management.",
                "skills": ["Data-Driven Decision-Making", "Power BI", "Python", "SQL", 
                          "Business Analysis", "Data Analysis"],
                "offers": ["Peer Support", "Collaboration", "Networking"],
                "asks": ["Networking and Support"]
            },
            {
                "name": "Nura Saloojee",
                "joined": "10/1/2025",
                "title": "Master of Business Analytics @ Schulich",
                "location": "Greater Toronto Area, Canada",
                "linkedin": "https://linkedin.com/in/nura-saloojee",
                "description": "BMath @ UWaterloo. Transform complex data into clear, actionable insights. Blend analytical rigour with creative problem-solving.",
                "skills": ["Python", "Pandas", "SQL", "Data Analysis", "Business Intelligence", 
                          "Data Visualization", "Machine Learning", "Statistical Analysis", "CRM", 
                          "Financial Analysis", "Market Research", "SWOT Analysis", "Salesforce", "Excel"],
                "offers": ["Networking"],
                "asks": ["Networking", "Keeping up with Schulich community"]
            }
        ]
    }
    
    # check if cohort data is available
    if year not in members_database:
        available_years = list(members_database.keys())
        return {
            "status": "error", 
            "message": f"No data available for MBAN cohort of {year}. Available years: {available_years}"
        }
    
    # retrieve the list of members for a unique cohort
    cohort_members = members_database[year]
    
    # collect data for members of a unique cohort
    all_skills = []
    locations = []
    
    # data collection loop
    for member in cohort_members:
        all_skills.extend(member.get("skills", [])) # get() returns an empty list if the key doesn't exist
        locations.append(member.get("location", ""))
    
    # count and rank skills
    skill_counts = Counter(all_skills) # count how many times each item appears in the list
    top_skills = dict(skill_counts.most_common(5)) # create a dictionary with the 5 most common skills
    
    # identify common characteristics
    trending_topics = []
    if "AI" in str(all_skills) or "Machine Learning" in str(all_skills):
        trending_topics.append("AI & Machine Learning")
    if "Business Intelligence" in str(all_skills) or "Business Analytics" in str(all_skills) or "Data Visualization" in str(all_skills):
        trending_topics.append("BI & Data Visualization")
    if any("Networking" in member.get("asks", []) for member in cohort_members):
        trending_topics.append("Professional Networking")
    
    
    # calculate statistics
    total_members = len(cohort_members) # count of alumni in a cohort
    
    # determine most common location
    normalized_locations = [normalize_city(loc) for loc in locations]
    location_counts = Counter(normalized_locations)
    primary_location = location_counts.most_common(1)[0][0] if location_counts else "NaN"
    primary_count = location_counts.most_common(1)[0][1] if location_counts else 0
    
    return {
        "status": "success",
        "data": {
            "total_alumni": total_members,
            "top_skills": top_skills,
            "primary_location": primary_location,
            "trending_topics": trending_topics,
            "member_highlights": [
                {
                    "name": member["name"],
                    "title": member["title"],
                    "linkedin": member["linkedin"]
                } for member in cohort_members[:3]  # Top 3 members
            ]
        }
    }

# define the agent
root_agent = Agent(
    model="gemini-2.0-flash",
    name="mban_dashboard_agent",
    description="Provides insights about MBAN cohorts at Schulich based on Dotsnet member data",
    instruction="""You are an agent that provides insights about MBAN (Master of Business Analytics) cohorts at Schulich School of Business based on data from Dotsnet.
    
    When a user asks for information about an MBAN cohort:
    1. Identify the year of the cohort from the user's query
    2. Use the 'get_info' tool to retrieve actual member data
    3. Provide a concise, professional summary (maximum 5 sentences)
    
    Your response should include:
    - Total number of members in the cohort
    - Top 5 skills across the cohort
    - Primary areas of focus
    
    Format the response to be actionable. Include actual member names and LinkedIn URLs when discussing connections.
    
    If data is not available for the requested year, politely inform the user and mention which years are available.
    
    Example query & response format:
    User: "Tell me about the MBAN 2026 cohort."
    Agent: "The MBAN 2026 cohort includes [X] members. The top skills are Python, SQL, Tableau, Workflow automation, and Business intelligence. Members primarily focus on financials with few members interested in healthcare or pharmaceuticals. The cohort is particularly engaged in applied AI projects. For networking, consider connecting with [other member] ([one-liner about other member]) at [LinkedIn URL]."

    User: "Do you have info for MBAN [year]]?"
    Agent: "Sorry, I don’t have data for the [year] MBAN cohort yet. I can currently provide insights for the 2025 cohort."

    User: "Summarize the 2026 cohort?"
    Agent: "The MBAN 2026 cohort currently has [X] active members. The cohort's top skills include [list key skills with counts]. Members are primarily focused on [top focus areas]. The cohort is actively engaged in [trending topics]. For networking, consider connecting with [member name] ([expertise area]) at [LinkedIn URL]."

    User: "What are the top skills of the 2026 cohort?"
    Agent: "The 2026 cohort has a diverse skillset with most members proficient in Python and SQL. Other core skills of the cohort are data visualization, case analysis, and effective communication of business insights."
    """,
    tools=[get_info]
)