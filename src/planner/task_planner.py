from typing import List, Dict, Any
from ..agent.autonomous_agent import Task, Goal
import networkx as nx
from datetime import datetime

class TaskPlanner:
    def __init__(self):
        self.dependency_graph = nx.DiGraph()

    def analyze_dependencies(self, tasks: List[Task]) -> nx.DiGraph:
        """Analyze task dependencies and create a directed graph."""
        self.dependency_graph.clear()
        
        # Add all tasks as nodes
        for task in tasks:
            self.dependency_graph.add_node(task.name, task=task)
        
        # Add edges based on dependencies
        for task in tasks:
            for dep in task.dependencies:
                if dep in self.dependency_graph:
                    self.dependency_graph.add_edge(dep, task.name)
        
        return self.dependency_graph

    def validate_dependencies(self) -> bool:
        """Check if the dependency graph is valid (no cycles)."""
        try:
            nx.find_cycle(self.dependency_graph)
            return False
        except nx.NetworkXNoCycle:
            return True

    def get_execution_order(self) -> List[str]:
        """Get the optimal execution order of tasks based on dependencies and priorities."""
        if not self.validate_dependencies():
            raise ValueError("Task dependencies contain cycles")

        # Use topological sort to get the base order
        base_order = list(nx.topological_sort(self.dependency_graph))
        
        # Sort tasks within each dependency level by priority
        sorted_tasks = []
        for task_name in base_order:
            task = self.dependency_graph.nodes[task_name]['task']
            sorted_tasks.append((task_name, task.priority))
        
        # Sort by priority (descending) while maintaining dependency order
        sorted_tasks.sort(key=lambda x: (-x[1], base_order.index(x[0])))
        
        return [task_name for task_name, _ in sorted_tasks]

    def estimate_completion_time(self, task: Task) -> float:
        """Estimate the time required to complete a task."""
        # This is a simple estimation based on task priority and dependencies
        base_time = 1.0 / task.priority
        dependency_factor = len(task.dependencies) * 0.2
        return base_time + dependency_factor

    def optimize_task_order(self, tasks: List[Task]) -> List[Task]:
        """Optimize the order of tasks based on dependencies, priorities, and estimated completion times."""
        self.analyze_dependencies(tasks)
        execution_order = self.get_execution_order()
        
        # Create a mapping of task names to task objects
        task_map = {task.name: task for task in tasks}
        
        # Return tasks in the optimized order
        return [task_map[name] for name in execution_order]

    def suggest_task_breakdown(self, goal: Goal) -> List[Task]:
        """Suggest a breakdown of tasks for a given goal."""
        # This is a simple implementation that can be enhanced with more sophisticated
        # task breakdown strategies
        tasks = []
        
        # Create main task
        main_task = Task(
            name=f"main_{goal.description.lower().replace(' ', '_')}",
            description=goal.description,
            priority=goal.priority
        )
        tasks.append(main_task)
        
        # Create sub-tasks for sub-goals
        for i, sub_goal in enumerate(goal.sub_goals):
            sub_task = Task(
                name=f"sub_{i}_{sub_goal.description.lower().replace(' ', '_')}",
                description=sub_goal.description,
                priority=sub_goal.priority,
                dependencies=[main_task.name]
            )
            tasks.append(sub_task)
        
        return tasks 