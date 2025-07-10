from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .init_llm import _default_llm  # provides the configured Gemini LLM
import os
from pathlib import Path
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class CreateWsiKl:
    """WSI Cancer Description Multi-Agent System"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # WSI Cancer Description Agents
    @agent
    def planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["planning_agent"],  # type: ignore[index]
            verbose=True,
            llm=_default_llm,
        )

    @agent
    def description_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["description_generator"],  # type: ignore[index]
            verbose=True,
            llm=_default_llm,
        )

    @agent
    def description_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["description_evaluator"],  # type: ignore[index]
            verbose=True,
            llm=_default_llm,
        )

    @agent
    def finalizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["finalizer_agent"],  # type: ignore[index]
            verbose=True,
            llm=_default_llm,
        )

    # WSI Cancer Description Tasks
    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["planning_task"],  # type: ignore[index]
        )

    @task
    def description_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config["description_generation_task"],  # type: ignore[index]
        )

    @task
    def description_evaluation_task(self) -> Task:
        return Task(
            config=self.tasks_config["description_evaluation_task"],  # type: ignore[index]
        )

    @task
    def finalization_task(self) -> Task:
        return Task(
            config=self.tasks_config["finalization_task"],  # type: ignore[index]
            output_file="wsi_cancer_description.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WSI Cancer Description Multi-Agent System"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # Initialize WSI Cancer knowledge sources
        knowledge_sources = []

        # Add PDF knowledge source if available
        pdf_files = [
            "sodapdf-converted.pdf",
            "wsi_cancer_knowledge.pdf",
            "pathology_reference.pdf",
        ]

        for pdf_file in pdf_files:
            pdf_path = Path("knowledge") / pdf_file
            if pdf_path.exists():
                knowledge_sources.append(CrewDoclingSource(file_paths=[str(pdf_path)]))

        # Add text knowledge sources
        text_files = [
            "user_preference.txt",
            "wsi_cancer_data.txt",
            "pathology_guidelines.txt",
        ]

        for text_file in text_files:
            text_path = Path("knowledge") / text_file
            if text_path.exists():
                knowledge_sources.append(CrewDoclingSource(file_paths=[str(text_path)]))

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # Sequential process ensures proper workflow: Planning -> Generation -> Evaluation -> Finalization
            knowledge_sources=knowledge_sources,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/text-embedding-004",
                    "api_key": os.getenv("GEMINI_API_KEY"),
                },
            },
        )
