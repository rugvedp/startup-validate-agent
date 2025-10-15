from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from startup_validate.tools.custom_tool import QuickChartTool
import os
load_dotenv()


@CrewBase
class StartupValidate():
    """StartupValidate crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        max_rpm=13,
        temperature=0,
        stop=["<stop>"]
    )


    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )

    @agent
    def competitive_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['competitive_researcher'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3 ,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )

    @agent
    def business_model_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_model_analyst'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3 ,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )

    @agent
    def funding_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['funding_analyst'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3 ,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )

    @agent
    def validation_scorer(self) -> Agent:
        return Agent(
            config=self.agents_config['validation_scorer'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(), QuickChartTool()],
            max_retry_limit=3 ,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )

    @agent
    def startup_validation_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['startup_validation_manager'], # type: ignore[index]
            verbose=True,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True,
            # output_file='output/startup_validation_report.md'
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_analysis_task'], # type: ignore[index]
            context=[self.tasks_config['competitive_analysis_task'], self.tasks_config['funding_analysis_task'], self.tasks_config['validation_scoring_task'] , self.tasks_config['business_model_task'],self.tasks_config['manager_report_task']]
        )

    @task
    def competitive_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['competitive_analysis_task'], # type: ignore[index]
            context=[self.tasks_config['market_analysis_task'], self.tasks_config['funding_analysis_task'], self.tasks_config['validation_scoring_task'] , self.tasks_config['business_model_task'],self.tasks_config['manager_report_task']]

        )

    @task
    def business_model_task(self) -> Task:
        return Task(
            config=self.tasks_config['business_model_task'], # type: ignore[index]
            context=[self.tasks_config['market_analysis_task'], self.tasks_config['funding_analysis_task'], self.tasks_config['validation_scoring_task'] , self.tasks_config['competitive_analysis_task'],self.tasks_config['manager_report_task']]

        )

    @task
    def funding_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['funding_analysis_task'], # type: ignore[index]
            context=[self.tasks_config['market_analysis_task'], self.tasks_config['business_model_task'], self.tasks_config['validation_scoring_task'] , self.tasks_config['competitive_analysis_task'],self.tasks_config['manager_report_task']]

        )

    @task
    def validation_scoring_task(self) -> Task:
        return Task(
            config=self.tasks_config['validation_scoring_task'], # type: ignore[index]
            context=[self.tasks_config['market_analysis_task'], self.tasks_config['business_model_task'], self.tasks_config['funding_analysis_task'] , self.tasks_config['competitive_analysis_task'],self.tasks_config['manager_report_task']]

            # output_file='startup_validation_report.md'
        )


    @task
    def manager_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['manager_report_task'], # type: ignore[index]
            context=[
                self.tasks_config['market_analysis_task'],
                self.tasks_config['competitive_analysis_task'],
                self.tasks_config['business_model_task'],
                self.tasks_config['funding_analysis_task'],
                self.tasks_config['validation_scoring_task']
            ]
        )


    @crew
    def crew(self) -> Crew:
        """Creates the StartupValidate crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.market_analyst(), self.competitive_researcher(), self.business_model_analyst(), self.funding_analyst(), self.validation_scorer()],
            tasks=[
                self.market_analysis_task(),
                self.competitive_analysis_task(),
                self.business_model_task(),
                self.funding_analysis_task(),
                self.validation_scoring_task(),
                self.manager_report_task()
            ],
            manager_agent=self.startup_validation_manager(),
            manager_llm=self.gemini_llm,
            process=Process.hierarchical,
            verbose=True,
            # memory=True,
            max_rpm=13,
            planning=True,
            planning_llm=self.gemini_llm,
            output_log_file = True,
            llm=self.gemini_llm,
            # embedder={
            #     "provider": "google-generativeai",
            #     "config": {
            #         "model": "models/text-embedding-001",
            #         "api_key": os.getenv("GEMINI_API_KEY")
            #     }
            # }
        )
