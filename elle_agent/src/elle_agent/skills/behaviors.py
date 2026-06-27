"""Behaviors skill — behavior tree and coordinator control."""

import subprocess
from typing import Optional

from ..launch_manager import LaunchManager
from ..state import ElleAgentState


class BehaviorsSkill:
    """Skills for behavior tree and coordinator management.

    The AMR uses a behavior tree (amr_tree_nodes.xml) managed by
    amr_behaviors_server and coordinated by amr_coordinator.
    The agent primarily interacts through these abstractions rather
    than directly with Nav2 nodes.
    """

    def __init__(self, launch_mgr: LaunchManager, state: ElleAgentState):
        self.launch_mgr = launch_mgr
        self.state = state

    def _run_service(self, service: str, srv_type: str = "std_srvs/srv/Empty") -> str:
        cmd = [
            "bash", "-c",
            f"source /opt/ros/humble/setup.bash && "
            f"source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 service call {service} {srv_type}"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.stdout + r.stderr if r.returncode == 0 else f"Failed: {r.stderr}"

    def start_bt_server(self, params_file: Optional[str] = None) -> str:
        """Start the AMR behavior tree server."""
        if self.launch_mgr.is_running("bt_server"):
            return "BT server already running"

        args = []
        if params_file:
            args.append(f"params_file:={params_file}")

        ok = self.launch_mgr.start_process(
            "bt_server",
            "amr_behaviors",
            "amr_behaviors_server.launch.py",
            args if args else None,
        )
        if ok:
            return "BT server started"
        return "Failed to start BT server"

    def stop_bt_server(self) -> str:
        """Stop the BT server."""
        if not self.launch_mgr.is_running("bt_server"):
            return "BT server not running"
        self.launch_mgr.stop_process("bt_server")
        return "BT server stopped"

    def start_coordinator(self, params_file: Optional[str] = None) -> str:
        """Start the AMR coordinator."""
        if self.launch_mgr.is_running("coordinator"):
            return "Coordinator already running"

        args = []
        if params_file:
            args.append(f"params_file:={params_file}")

        ok = self.launch_mgr.start_process(
            "coordinator",
            "amr_coordinator",
            "amr_coordinator.launch.py",
            args if args else None,
        )
        if ok:
            return "Coordinator started"
        return "Failed to start coordinator"

    def stop_coordinator(self) -> str:
        """Stop the AMR coordinator."""
        if not self.launch_mgr.is_running("coordinator"):
            return "Coordinator not running"
        self.launch_mgr.stop_process("coordinator")
        return "Coordinator stopped"

    def start_middleware(self, params_file: Optional[str] = None) -> str:
        """Start the AMR middleware server."""
        if self.launch_mgr.is_running("middleware"):
            return "Middleware already running"

        args = []
        if params_file:
            args.append(f"params_file:={params_file}")

        ok = self.launch_mgr.start_process(
            "middleware",
            "amr_middleware",
            "amr_middleware.launch.py",
            args if args else None,
        )
        if ok:
            return "Middleware started"
        return "Failed to start middleware"

    def stop_middleware(self) -> str:
        """Stop the AMR middleware."""
        if not self.launch_mgr.is_running("middleware"):
            return "Middleware not running"
        self.launch_mgr.stop_process("middleware")
        return "Middleware stopped"

    def reset_buttons(self) -> str:
        """Reset coordinator buttons via service."""
        return self._run_service("/reset_buttons")

    def pause_drive(self) -> str:
        """Pause the drive behavior in BT."""
        return self._run_service("/pause_drive")

    def resume_drive(self) -> str:
        """Resume the drive behavior in BT."""
        return self._run_service("/resume_drive")

    def speed_limit(self, limit: float = 0.5) -> str:
        """Apply speed limit (m/s)."""
        cmd = [
            "bash", "-c",
            f"source /opt/ros/humble/setup.bash && "
            f"source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 param set /bt_navigator speed_limit {limit}"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return f"Speed limit set to {limit} m/s"
        return f"Failed: {r.stderr}"

    def full_bringup(
        self,
        robot_model: Optional[str] = None,
        use_sim_time: bool = True,
    ) -> str:
        """Start full robot bringup: middleware + coordinator + behaviors."""
        results = []

        results.append(self.start_middleware())
        results.append(self.start_coordinator())
        results.append(self.start_bt_server())

        return " | ".join(results)
