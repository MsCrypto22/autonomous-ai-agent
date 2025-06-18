from src.agent.autonomous_agent import AutonomousAgent, Task, Goal
from src.planner.task_planner import TaskPlanner

def main():
    # Initialize the agent
    agent = AutonomousAgent()
    planner = TaskPlanner()

    # Set a main goal
    main_goal = Goal(
        description="Complete project documentation",
        priority=1,
        sub_goals=[
            Goal(description="Write README", priority=2),
            Goal(description="Create API documentation", priority=2),
            Goal(description="Add usage examples", priority=1)
        ]
    )
    agent.set_goal(main_goal.description, main_goal.priority)

    # Get suggested task breakdown
    tasks = planner.suggest_task_breakdown(main_goal)
    
    # Add tasks to the agent
    for task in tasks:
        agent.add_task(task)

    # Run the agent
    print("Starting agent execution...")
    agent.run()
    
    # Print final state
    print("\nFinal agent state:")
    state = agent.get_state()
    print(f"Current goal: {state['current_goal']['description']}")
    print(f"Completed tasks: {state['completed_tasks']}")
    print(f"Pending tasks: {state['pending_tasks']}")

if __name__ == "__main__":
    main() 