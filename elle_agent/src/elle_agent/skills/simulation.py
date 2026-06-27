"""Simulation skill — start/stop/reset Gazebo simulation."""

from typing import Optional

from ..launch_manager import LaunchManager
from ..state import ElleAgentState, RobotMode


class SimulationSkill:
    """Skills for controlling Gazebo simulation lifecycle."""

    def __init__(self, launch_mgr: LaunchManager, state: ElleAgentState):
        self.launch_mgr = launch_mgr
        self.state = state

    def start(
        self,
        world: str = "DefaultWorld",
        robot_model: Optional[str] = None,
        gui: bool = True,
    ) -> str:
        """Start simulation world with robot model."""
        if self.state.simulation.running:
            return f"Simulation already running: {self.state.simulation.world_name}"

        model = robot_model or self.state.simulation.robot_model
        if model not in self.state.SUPPORTED_MODELS:
            return f"Unknown robot model: {model}. Supported: {self.state.SUPPORTED_MODELS}"

        ok = self.launch_mgr.start_simulation(
            world_name=world,
            robot_model=model,
            use_gz_gui=gui,
        )
        if ok:
            return f"Simulation started: {world} with {model}"
        return "Failed to start simulation"

    def stop(self) -> str:
        """Stop simulation and clean up processes."""
        self.launch_mgr.stop_simulation()
        return "Simulation stopped"

    def reset(self) -> str:
        """Reset simulation (stop + start with same params)."""
        world = self.state.simulation.world_name
        model = self.state.simulation.robot_model
        self.launch_mgr.stop_simulation()
        self.launch_mgr.start_simulation(world_name=world, robot_model=model)
        return f"Simulation reset: {world} with {model}"

    def status(self) -> str:
        """Get simulation status."""
        return self.state.summary()
