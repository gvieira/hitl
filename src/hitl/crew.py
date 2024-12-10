import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, after_kickoff, agent, before_kickoff, crew, task
from crewai.tools import tool

# Uncomment the following line to use an example of a custom tool
# from hitl.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@tool
def dumb_tool() -> str:
    """Use this tool to come up with a dumb output"""
    dumb_value = os.getenv("SOMETHING", "default")
    return f"Dumb output: {dumb_value}"


@CrewBase
class Hitl:
    """Hitl crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def inventor(self) -> Agent:
        return Agent(
            config=self.agents_config["inventor"],
            # tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
            verbose=True,
        )

    @agent
    def mathematician(self) -> Agent:
        return Agent(config=self.agents_config["mathematician"], verbose=True)

    @task
    def dumb_task(self) -> Task:
        return Task(
            config=self.tasks_config["dumb_task"],
            tools=[dumb_tool],
        )

    @task
    def invent_two_numbers(self) -> Task:
        return Task(
            config=self.tasks_config["invent_two_numbers"],
            # human_input=True,
        )

    @task
    def sum_two_numbers(self) -> Task:
        return Task(
            config=self.tasks_config["sum_two_numbers"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Hitl crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
