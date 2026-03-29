from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Agents

profile_agent = Agent(
    role="Career Profile Analyzer",
    goal="Analyze resume and identify skills + gaps",
    backstory="Expert AI career coach",
    llm=llm,
    verbose=True
)

market_agent = Agent(
    role="Market Research Analyst",
    goal="Find trending skills for given role",
    backstory="Tech job market expert",
    llm=llm,
    verbose=True
)

roadmap_agent = Agent(
    role="Roadmap Planner",
    goal="Create structured learning roadmap",
    backstory="Mentor with 10+ years experience",
    llm=llm,
    verbose=True
)

resource_agent = Agent(
    role="Resource Finder",
    goal="Suggest free courses and YouTube videos",
    backstory="Online learning expert",
    llm=llm,
    verbose=True
)


def run_crew(resume_text, goal):

    # Task 1 → Profile Analysis
    task1 = Task(
        description=f"""
        Analyze the resume for goal: {goal}

        Extract:
        - Current Skills
        - Strengths
        - Missing Skills

        Resume:
        {resume_text}
        """,
        expected_output="""
        A structured analysis containing:
        - List of current skills
        - Strengths
        - Missing skills (skill gaps)
        """,
        agent=profile_agent
    )

    # Task 2 → Uses output of Task 1
    task2 = Task(
        description=f"""
        Based on the previous analysis, identify:

        - Top trending skills for {goal}
        - Industry requirements

        Use the identified skill gaps to guide your response.
        """,
        expected_output="""
        - Top 10 trending skills
        - Industry requirements
        """,
        agent=market_agent,
        context=[task1] 
    )

    # Task 3 → Uses Task 1 + Task 2
    task3 = Task(
        description="""
        Create a structured roadmap using skill gaps and trends using:

        - Skill gaps (from analysis)
        - Market trends

        Format:
        - 0–1 month
        - 1–3 months
        - 3–6 months
        """,
        expected_output="""
        A roadmap divided into:
        - 0–1 month
        - 1–3 months
        - 3–6 months
        """,
        agent=roadmap_agent,
        context=[task1, task2]   
    )

    # Task 4 → Uses Task 3
    task4 = Task(
        description="""
        Suggest learning resources based on roadmap
        Generate FINAL output in STRICT JSON format.

        Use previous outputs:
        - Skills
        - Missing Skills
        - Trending Skills
        - Roadmap

        FORMAT:

        {{
        "skills": [],
        "missing_skills": [],
        "trending_skills": [],
        "roadmap": {{
            "0-1_month": [],
            "1-3_months": [],
            "3-6_months": []
        }},
        "resources": {{
            "courses": [
            {{"title": "", "link": ""}}
            ],
            "youtube": [
            {{"title": "Deep Learning Tutorial", "link": "SEARCH: deep learning python"}},
            {{"title": "Machine Learning Basics", "link": "SEARCH: machine learning tutorial"}}
            ],
            "practice": [
            {{"title": "Kaggle", "link": "https://www.kaggle.com"}},
            {{"title": "LeetCode", "link": "https://leetcode.com"}}
            ]
            
        }}
        }}

        IMPORTANT:
        - For YouTube, DO NOT give direct links
        - Always use format: "SEARCH: topic"
        - Example: "SEARCH: deep learning python tutorial"
        - Output ONLY JSON (no explanation)
        """,
    
        expected_output="Structured JSON output",
        agent=resource_agent,
        context=[task1, task2, task3] 
    )

    # Crew Execution
    crew = Crew(
        agents=[profile_agent, market_agent, roadmap_agent, resource_agent],
        tasks=[task1, task2, task3, task4],
        verbose=True
    )

    result = crew.kickoff()
    return result

