from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any, Optional
from .init_llm import _default_llm  # provides the configured Gemini LLM
import os
import json
from pathlib import Path
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class CreateWsiKl:
    """WSI Cancer Description Multi-Agent System"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self, use_json_source: bool = False, json_file_path: Optional[str] = None):
        """Initialize the crew with optional JSON data source
        
        Args:
            use_json_source: If True, use JSON file as knowledge source instead of PDFs
            json_file_path: Path to JSON file containing cancer descriptions
        """
        super().__init__()
        self.use_json_source = use_json_source
        self.json_file_path = json_file_path

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

    def load_json_descriptions(self, file_path: str) -> Dict[str, Any]:
        """Load cancer descriptions from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"JSON file not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            return {}

    @crew
    def crew(self) -> Crew:
        """Creates the WSI Cancer Description Multi-Agent System"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        # Initialize WSI Cancer knowledge sources
        knowledge_sources = []

        if self.use_json_source and self.json_file_path:
            # Scenario 2: Use JSON file as knowledge source
            json_descriptions = self.load_json_descriptions(self.json_file_path)
            if json_descriptions:
                # Convert JSON descriptions to string format for knowledge source
                descriptions_text = ""
                for cancer_type, descriptions in json_descriptions.items():
                    descriptions_text += f"\n\n=== {cancer_type} ===\n"
                    if isinstance(descriptions, list):
                        for desc in descriptions:
                            descriptions_text += f"- {desc}\n"
                    else:
                        descriptions_text += f"{descriptions}\n"
                
                knowledge_sources.append(
                    StringKnowledgeSource(
                        content=descriptions_text,
                        metadata={"source": "json_cancer_descriptions"}
                    )
                )
        else:
            # Scenario 1: Use PDF files as knowledge source
            # Absolute path for existence check
            _abs_knowledge_dir = Path(__file__).resolve().parents[2] / "knowledge"

            # List of knowledge files to load (add new filenames here as needed)
            knowledge_files = [
                "camelyon16.pdf",
                "tcga_lung.pdf", 
                "tcga_renal.pdf",
                "Pathoma 2021 - Kidney.pdf",
            ]

            for fname in knowledge_files:
                abs_path = _abs_knowledge_dir / fname  # absolute path for validation
                rel_path = (
                    fname  # path relative to knowledge dir handled internally by CrewAI
                )
                if abs_path.exists():
                    knowledge_sources.append(CrewDoclingSource(file_paths=[str(rel_path)]))

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
