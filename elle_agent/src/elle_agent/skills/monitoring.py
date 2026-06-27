"""Monitoring skill — robot status, sensors, BT, costmaps."""

from typing import Dict, Optional

from ..launch_manager import LaunchManager
from ..state import (
    BtStatus,
    ElleAgentState,
    NodeOverallStatus,
    NodeStatus,
    SensorStatus,
)
from ..topics import TopicMonitor


class MonitoringSkill:
    """Skills for monitoring robot state and health."""

    def __init__(
        self,
        launch_mgr: LaunchManager,
        state: ElleAgentState,
        monitor: TopicMonitor,
    ):
        self.launch_mgr = launch_mgr
        self.state = state
        self.monitor = monitor

    def start_monitoring(self):
        """Start all background monitor threads."""
        self.monitor.monitor_emergency_stop()
        self.monitor.monitor_node_status()
        self.monitor.monitor_bt_status()
        self.monitor.monitor_sensors()

    def stop_monitoring(self):
        """Stop all monitor threads."""
        self.monitor.stop_all()

    def emergency_stop_status(self) -> str:
        """Get emergency stop state."""
        active = self.state.robot_status.emergency_stop
        return "🛑 EMERGENCY STOP ACTIVE" if active else "✅ Emergency stop clear"

    def trigger_emergency_stop(self) -> str:
        """Trigger emergency stop via topic."""
        from ..topics import TopicPublisher
        pub = TopicPublisher()
        pub.emergency_stop(active=True)
        self.state.robot_status.emergency_stop = True
        return "Emergency stop triggered"

    def clear_emergency_stop(self) -> str:
        """Clear emergency stop flag."""
        from ..topics import TopicPublisher
        pub = TopicPublisher()
        pub.emergency_stop(active=False)
        self.state.robot_status.emergency_stop = False
        return "Emergency stop cleared"

    def node_status(self) -> str:
        """Get all node statuses."""
        nodes = self.state.robot_status.nodes
        if not nodes:
            return "No node status data (not monitoring or no data)"
        lines = []
        for name, node in nodes.items():
            icon = "✅" if node.status == NodeOverallStatus.OK else "⚠️" if node.status == NodeOverallStatus.WARNING else "❌"
            lines.append(f"{icon} {name}: {node.status.value} {node.error_code}")
        return "\n".join(lines)

    def sensor_status(self) -> str:
        """Get all sensor statuses."""
        sensors = self.state.robot_status.sensors
        if not sensors:
            return "No sensor data"
        lines = []
        for name, sensor in sensors.items():
            icon = "✅" if sensor.status == "ok" else "⚠️"
            lines.append(f"{icon} {name}: {sensor.status} = {sensor.value}")
        return "\n".join(lines)

    def bt_status(self) -> str:
        """Get behavior tree status."""
        bt = self.state.robot_status.bt_status
        if bt.status.value == "idle":
            return "BT: idle"
        icon = "▶️" if bt.status.value == "running" else "✅" if bt.status.value == "success" else "❌"
        return f"{icon} BT: {bt.current_node} [{bt.status.value}] — {bt.message}"

    def costmap_status(self) -> str:
        """Check if costmap topics are publishing."""
        local_ok = self.monitor.monitor_costmap("/local_costmap/costmap")
        global_ok = self.monitor.monitor_costmap("/global_costmap/costmap")
        local_icon = "✅" if local_ok else "❌"
        global_icon = "✅" if global_ok else "❌"
        return f"Local costmap: {local_icon} | Global costmap: {global_icon}"

    def full_status(self) -> str:
        """Get complete system status."""
        parts = [
            self.state.summary(),
            "",
            self.emergency_stop_status(),
            "",
            "Nodes:",
            self.node_status() or "(no data)",
            "",
            "Sensors:",
            self.sensor_status() or "(no data)",
            "",
            "BT:",
            self.bt_status(),
            "",
            "Costmaps:",
            self.costmap_status(),
        ]
        return "\n".join(parts)

    def is_safe(self) -> str:
        """Check if robot is safe to operate."""
        safe = self.state.is_safe()
        return "✅ Robot is safe" if safe else "🛑 Safety check FAILED"
