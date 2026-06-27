"""Navigation skill — SLAM, localization, Nav2 navigation control."""

import subprocess
import time
from typing import Optional

from ..launch_manager import LaunchManager
from ..state import ElleAgentState, NavigationStatus, RobotMode
from ..topics import TopicMonitor, TopicPublisher


class NavigationSkill:
    """Skills for mapping, localization, and navigation."""

    def __init__(
        self,
        launch_mgr: LaunchManager,
        state: ElleAgentState,
        monitor: TopicMonitor,
        publisher: TopicPublisher,
    ):
        self.launch_mgr = launch_mgr
        self.state = state
        self.monitor = monitor
        self.publisher = publisher

    # ─── SLAM / Mapping ────────────────────────────────────────

    def start_slam(
        self,
        method: str = "slam_toolbox",
        rviz: bool = False,
    ) -> str:
        """Start SLAM mapping."""
        if self.state.mapping.active:
            return "SLAM already active"
        if method not in ("slam_toolbox", "cartographer"):
            return f"Unknown SLAM method: {method}"

        ok = self.launch_mgr.start_slam(method=method, open_rviz=rviz)
        if ok:
            return f"SLAM started ({method})"
        return "Failed to start SLAM"

    def stop_slam(self) -> str:
        """Stop SLAM mapping."""
        if not self.state.mapping.active:
            return "SLAM not active"
        self.launch_mgr.stop_slam()
        return "SLAM stopped"

    def save_map(self, path: str) -> str:
        """Save current map to disk via nav2_map_server."""
        if not self.state.mapping.active:
            return "SLAM not active — nothing to save"

        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 run nav2_map_server map_saver_cli -f {path}"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            self.state.mapping.map_saved = True
            self.state.mapping.map_path = path
            return f"Map saved to {path}"
        return f"Failed to save map: {r.stderr}"

    def load_map(self, path: str) -> str:
        """Load a pre-saved map."""
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 run nav2_map_server map_server {path}"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            self.state.localization.map_loaded = True
            return f"Map loaded: {path}"
        return f"Failed to load map: {r.stderr}"

    # ─── Localization ───────────────────────────────────────────

    def start_localization(
        self,
        map_path: Optional[str] = None,
        rviz: bool = False,
    ) -> str:
        """Start AMCL localization."""
        if self.state.localization.active:
            return "Localization already active"

        ok = self.launch_mgr.start_localization(
            map_path=map_path,
            open_rviz=rviz,
        )
        if ok:
            return f"Localization started" + (f" with {map_path}" if map_path else "")
        return "Failed to start localization"

    def stop_localization(self) -> str:
        """Stop localization."""
        if not self.state.localization.active:
            return "Localization not active"
        self.launch_mgr.stop_localization()
        return "Localization stopped"

    def reset_localization(self) -> str:
        """Reset AMCL particle cloud."""
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            "ros2 service call /reset_localization std_srvs/srv/Empty"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return "Localization reset"
        return f"Failed: {r.stderr}"

    # ─── Navigation ─────────────────────────────────────────────

    def start_navigation(self) -> str:
        """Start Nav2 navigation stack."""
        if self.state.navigation.active:
            return "Navigation already active"

        ok = self.launch_mgr.start_navigation()
        if ok:
            self.state.navigation.status = NavigationStatus.IDLE
            return "Navigation stack started"
        return "Failed to start navigation"

    def stop_navigation(self) -> str:
        """Stop navigation stack."""
        if not self.state.navigation.active:
            return "Navigation not active"
        self.launch_mgr.stop_navigation()
        return "Navigation stopped"

    def navigate_to(
        self,
        x: float,
        y: float,
        z: float = 0.0,
        wait: bool = True,
        timeout: float = 60.0,
    ) -> str:
        """Navigate robot to (x, y, z) pose."""
        if not self.state.navigation.active:
            return "Navigation not active — start_navigation() first"

        self.publisher.goal_pose(x, y, z)
        self.state.navigation.status = NavigationStatus.RUNNING

        if wait:
            # Poll navigation status until complete or timeout
            start = time.time()
            while time.time() - start < timeout:
                if self.state.navigation.status in (
                    NavigationStatus.SUCCEEDED,
                    NavigationStatus.FAILED,
                ):
                    break
                time.sleep(1.0)

            if self.state.navigation.status == NavigationStatus.SUCCEEDED:
                return f"Navigation succeeded: ({x}, {y}, {z})"
            elif self.state.navigation.status == NavigationStatus.FAILED:
                return f"Navigation failed"
            else:
                return f"Navigation timeout after {timeout}s"
        else:
            return f"Goal sent: ({x}, {y}, {z})"

    def pause_navigation(self) -> str:
        """Pause current navigation."""
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            "ros2 service call /pause_navigation std_srvs/srv/Empty"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            self.state.navigation.status = NavigationStatus.PAUSED
            return "Navigation paused"
        return f"Failed: {r.stderr}"

    def resume_navigation(self) -> str:
        """Resume paused navigation."""
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            "ros2 service call /resume_navigation std_srvs/srv/Empty"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            self.state.navigation.status = NavigationStatus.RUNNING
            return "Navigation resumed"
        return f"Failed: {r.stderr}"

    def clear_costmaps(self) -> str:
        """Clear both global and local costmaps."""
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            "ros2 service call /clear_costmap std_srvs/srv/Empty"
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            return "Costmaps cleared"
        return f"Failed: {r.stderr}"

    # ─── Status ─────────────────────────────────────────────────

    def status(self) -> str:
        """Get full navigation status."""
        return self.state.summary()
