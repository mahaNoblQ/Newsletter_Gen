from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from typing import Dict, List, Tuple, Union
from langchain_core.agents import AgentFinish
from langchain_openai import ChatOpenAI

from newsletter_gen.tools.research import Search, FindSimilar, GetContents

import datetime
import json
import os

@CrewBase
class NewsletterGenCrew:
    """NewsletterGen crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatOpenAI(api_key=os.environ['OPENAI_API_KEY'], model='gpt-4-turbo')
        return llm

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[Search(), FindSimilar(), GetContents()],
            verbose=True,
            llm=self.llm(),
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            tools=[Search(), FindSimilar(), GetContents()],
            llm=self.llm(),
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config["designer"],
            verbose=True,
            llm=self.llm(),
            allow_delegation=False,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            output_file=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_research_task.md',
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config["edit_task"],
            agent=self.editor(),
            output_file=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_edit_task.md',
        )

    @task
    def newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config["newsletter_task"],
            agent=self.designer(),
            output_file=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_newsletter.html',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
