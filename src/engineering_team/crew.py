from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import logging
from crewai.task import TaskOutput

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Remove existing handlers (like StreamHandler from CrewAI)
if logger.hasHandlers():
    logger.handlers.clear()

# Create handlers
file_handler = logging.FileHandler('app.log')
console_handler = logging.StreamHandler()

# Create formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def on_task_complete(output: TaskOutput):
    logging.info(f"Task completed: {output.name}")
    logging.info(f"Agent: {output.agent}")
    # logging.info(f"Raw Output: {output.raw}")
    logging.info(f"Summary: {output.summary}")

def on_agent_step(step):
    print("biiiiiiiii")
    # print(dir(step))
    # logging.info(f"🔵 Agent Step → {step.get('agent_name', 'Unknown')} executed an action")
    logging.info(f"   Thought: {step.get('thought')}")
    logging.info(f"   Output: {step.get('output')}")
    # logging.info(f"   Observation: {step.get('observation')}")

@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @agent
    def documentation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_engineer'],
            verbose=True
        )
    
    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'],
            verbose=True
        )
    
    @agent
    def review_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['review_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def refactor_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['refactor_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )   

    @task
    def documentation_task(self) -> Task:
        return Task(
            config=self.tasks_config['documentation_task'],
        ) 
    
    @task
    def orchestrate_task(self) -> Task:
        return Task(
            config=self.tasks_config['orchestrate_task'],
        ) 
    
    @task
    def review_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_code_task'],
        ) 
    
    @task
    def refactor_code_task(self) -> Task:
        return Task(
            config=self.tasks_config['refactor_code_task'],
        ) 
      
    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        
        orchestrator_agent = self.orchestrator()

        agents_without_manager = [
            agent for agent in self.agents
            if agent is not orchestrator_agent
        ]
        
        return Crew(
            agents=agents_without_manager,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=orchestrator_agent,
            verbose=True,
            task_callback=on_task_complete,
            step_callback=on_agent_step,
        )