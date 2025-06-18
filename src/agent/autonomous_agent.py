from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

class Goal(BaseModel):
    description: str
    priority: int
    created_at: datetime = datetime.now()
    completed: bool = False
    sub_goals: List['Goal'] = []

class Task(BaseModel):
    name: str
    description: str
    status: str = "pending"
    priority: int = 1
    dependencies: List[str] = []
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None

class AutonomousAgent:
    def __init__(self):
        self.current_goal: Optional[Goal] = None
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.state: Dict[str, Any] = {}
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("AutonomousAgent")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def set_goal(self, description: str, priority: int = 1) -> None:
        """Set a new goal for the agent."""
        self.current_goal = Goal(description=description, priority=priority)
        self.logger.info(f"New goal set: {description}")

    def add_task(self, task: Task) -> None:
        """Add a new task to the queue."""
        self.task_queue.append(task)
        self.logger.info(f"New task added: {task.name}")

    def plan(self) -> None:
        """Plan the execution of tasks based on current goal and state."""
        if not self.current_goal:
            self.logger.warning("No goal set. Cannot plan.")
            return

        # Sort tasks by priority and dependencies
        self.task_queue.sort(key=lambda x: (x.priority, len(x.dependencies)))

    def execute_task(self, task: Task) -> bool:
        """Execute a single task and update its status."""
        try:
            self.logger.info(f"Executing task: {task.name}")
            # Task execution logic will be implemented here
            task.status = "completed"
            task.completed_at = datetime.now()
            self.completed_tasks.append(task)
            return True
        except Exception as e:
            self.logger.error(f"Error executing task {task.name}: {str(e)}")
            task.status = "failed"
            return False

    def run(self) -> None:
        """Main execution loop of the agent."""
        if not self.current_goal:
            self.logger.error("No goal set. Cannot run.")
            return

        while self.task_queue:
            self.plan()
            current_task = self.task_queue.pop(0)
            success = self.execute_task(current_task)
            
            if not success:
                self.logger.warning(f"Task {current_task.name} failed. Requeuing...")
                self.task_queue.append(current_task)

        self.logger.info("All tasks completed.")

    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent."""
        return {
            "current_goal": self.current_goal.dict() if self.current_goal else None,
            "pending_tasks": len(self.task_queue),
            "completed_tasks": len(self.completed_tasks),
            "state": self.state
        } 