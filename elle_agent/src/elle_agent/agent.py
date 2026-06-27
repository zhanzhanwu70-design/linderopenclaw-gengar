"""ELLE Agent — main agent class tying all skills together."""

from .launch_manager import LaunchManager
from .state import ElleAgentState
from .topics import TopicMonitor, TopicPublisher
from .skills.simulation import SimulationSkill
from .skills.navigation import NavigationSkill
from .skills.monitoring import MonitoringSkill
from .skills.behaviors import BehaviorsSkill


class ElleAgent:
    """Autonomous agent for operating ELLE_WS (ROS2 Humble AMR workspace).

    Usage:
        agent = ElleAgent()
        agent.simulation.start("WarehouseWorld")
        agent.navigation.start_navigation()
        agent.navigation.navigate_to(5.0, 3.0)
        print(agent.monitoring.full_status())
        agent.shutdown()
    """

    def __init__(self):
        self.state = ElleAgentState()
        self.launch_mgr = LaunchManager(self.state)
        self.monitor = TopicMonitor(self.state)
        self.publisher = TopicPublisher()

        # Skills
        self.simulation = SimulationSkill(self.launch_mgr, self.state)
        self.navigation = NavigationSkill(
            self.launch_mgr, self.state, self.monitor, self.publisher
        )
        self.monitoring = MonitoringSkill(self.launch_mgr, self.state, self.monitor)
        self.behaviors = BehaviorsSkill(self.launch_mgr, self.state)

        # Auto-start monitoring
        self.monitoring.start_monitoring()

    def shutdown(self):
        """Stop all processes and monitoring."""
        self.monitoring.stop_monitoring()
        self.launch_mgr.stop_all()

    def status(self) -> str:
        """Get full agent status."""
        return self.state.summary()

    def reset(self):
        """Full reset — stop everything and return to idle."""
        self.shutdown()
        self.state = ElleAgentState()
        # Re-initialize
        self.launch_mgr = LaunchManager(self.state)
        self.monitor = TopicMonitor(self.state)
        self.publisher = TopicPublisher()
        self.monitoring.start_monitoring()
