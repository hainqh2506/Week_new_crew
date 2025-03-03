from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from models.llm import togetherai_llm, gemini_llm
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.research_tool import SearchAndContents, FindSimilar, GetContents
from models.data import custom_model
# Khởi tạo LLM
LLM = togetherai_llm()
@CrewBase
class WeeklyNewsUpdateCrew: 
    """
    Weekly News Update Crew
    """
    
    # Định nghĩa config files
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def content_manager(self) -> Agent: 
        return Agent(
            config=self.agents_config["content_manager"],
            llm=LLM,
            verbose=True,
            memory=True
        )

    @task
    def content_ideation_task(self) -> Task: 
        return Task(
            config=self.tasks_config["content_ideation_task"],
            agent=self.content_manager(),
            output_pydantic=custom_model,
            Verbose=True,
            output_file="output/idea.json" #lưu ý tưởng vào file idea.json
        )
        
    @crew
    def crew(self) -> Crew: #crew tạo ý tưởng
        """
        Creates the Weekly News Update Crew
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )