"""Topic subscriber/publisher for ELLE_WS monitoring.

Lightweight monitoring only — uses subprocess `ros2 topic` commands
rather than a full rclpy node to keep dependencies minimal.
"""

import json
import subprocess
import threading
import time
from typing import Any, Callable, Dict, List, Optional

from .state import (
    BtNodeStatus,
    BtStatus,
    ElleAgentState,
    NodeOverallStatus,
    NodeStatus,
    SensorStatus,
)


class TopicMonitor:
    """Monitor ROS2 topics using `ros2 topic` subprocess."""

    def __init__(self, state: ElleAgentState):
        self.state = state
        self._callbacks: Dict[str, List[Callable]] = {}
        self._stop_events: Dict[str, threading.Event] = {}
        self._threads: Dict[str, threading.Thread] = {}

    def _run(self, args: List[str], timeout: int = 5) -> str:
        cmd = [
            "bash", "-c",
            "source /opt/ros/humble/setup.bash && "
            "source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 topic {' '.join(args)}"
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return r.stdout.strip()
        except (subprocess.TimeoutExpired, Exception):
            return ""

    def echo(self, topic: str, once: bool = True) -> str:
        """Echo a single message from a topic."""
        args = [topic, " "--ot"] if once else [topic]
        return self._run(["echo", topic, "--once"] if once else ["echo", topic])

    def list(self) -> List[str]:
        """List all active topics."""
        out = self._run(["list"])
        return [l.strip() for l in out.split("\n") if l.strip()]

    def hz(self, topic: str) -> Optional[float]:
        """Get approximate topic rate in Hz."""
        out = self._run(["hz", topic, "--window", "5"])
        # Parse "average rate: 10.234" from output
        for line in out.split("\n"):
            if "average rate:" in line:
                try:
                    return float(line.split("average rate:")[1].split()[0])
                except (IndexError, ValueError):
                    pass
        return None

    def find(self, topic_type: str) -> List[str]:
        """Find topics by type."""
        out = self._run(["find", topic_type])
        return [l.strip() for l in out.split("\n") if l.strip()]

    def bw(self, topic: str) -> Optional[str]:
        """Get topic bandwidth."""
        out = self._run(["bw", topic, "--window", "5"])
        return out

    # ─── Monitored topics ───────────────────────────────────────

    def monitor_emergency_stop(self, callback: Optional[Callable] = None):
        """Monitor /emergency_stop topic."""
        def poll():
            while True:
                out = self.echo("/emergency_stop", once=True)
                val = "true" in out.lower() if out else False
                self.state.robot_status.emergency_stop = val
                if callback:
                    callback(val)
                time.sleep(1.0)

        t = threading.Thread(target=poll, daemon=True)
        t.start()
        self._threads["emergency_stop"] = t

    def monitor_node_status(self):
        """Poll /node_status for coordinator node states."""
        def poll():
            while True:
                out = self.echo("/node_status", once=True)
                if out:
                    try:
                        # Expect JSON or parseable format
                        data = json.loads(out)
                        for item in data.get("nodes", []):
                            ns = NodeStatus(
                                name=item.get("node_name", ""),
                                status=NodeOverallStatus(item.get("status", "unknown")),
                                error_code=item.get("error_code", ""),
                            )
                            self.state.robot_status.nodes[item["node_name"]] = ns
                    except (json.JSONDecodeError, ValueError):
                        pass
                time.sleep(2.0)

        t = threading.Thread(target=poll, daemon=True)
        t.start()
        self._threads["node_status"] = t

    def monitor_bt_status(self):
        """Poll /behavior_tree_logger for BT execution state."""
        def poll():
            while True:
                out = self.echo("/behavior_tree_logger", once=True)
                if out:
                    try:
                        data = json.loads(out)
                        self.state.robot_status.bt_status = BtStatus(
                            current_node=data.get("current_node", ""),
                            status=BtNodeStatus(data.get("status", "idle")),
                            message=data.get("message", ""),
                        )
                    except (json.JSONDecodeError, ValueError):
                        pass
                time.sleep(1.0)

        t = threading.Thread(target=poll, daemon=True)
        t.start()
        self._threads["bt_status"] = t

    def monitor_sensors(self):
        """Poll /sensors_status for sensor states."""
        def poll():
            while True:
                out = self.echo("/sensors_status", once=True)
                if out:
                    try:
                        data = json.loads(out)
                        for item in data.get("sensors", []):
                            ss = SensorStatus(
                                name=item.get("sensor_name", ""),
                                status=item.get("status", "unknown"),
                                value=item.get("value", 0.0),
                            )
                            self.state.robot_status.sensors[item["sensor_name"]] = ss
                    except (json.JSONDecodeError, ValueError):
                        pass
                time.sleep(2.0)

        t = threading.Thread(target=poll, daemon=True)
        t.start()
        self._threads["sensors"] = t

    def monitor_costmap(self, topic: str = "/local_costmap/costmap"):
        """Check if costmap topic is publishing (indicates navigation active)."""
        rate = self.hz(topic)
        return rate is not None and rate > 0.1

    def stop_all(self):
        """Stop all monitor threads."""
        for name in list(self._threads.keys()):
            if name in self._stop_events:
                self._stop_events[name].set()
        self._threads.clear()


class TopicPublisher:
    """Publish to ROS2 topics using `ros2 topic pub`."""

    def __init__(self):
        pass

    def _run(self, args: List[str], data: str, once: bool = True) -> str:
        cmd = [
            "bash", "-c",
            f"source /opt/ros/humble/setup.bash && "
            f"source /home/node/elle_ws/install/local_setup.bash 2>/dev/null && "
            f"ros2 topic pub --once " if once else "ros2 topic pub "
            f"{' '.join(args)} '{data}'"
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return r.stdout + r.stderr
        except Exception as e:
            return str(e)

    def cmd_vel(self, linear: float = 0.0, angular: float = 0.0, once: bool = True):
        """Publish velocity command."""
        data = f"{{linear: {{x: {linear}, y: 0.0, z: 0.0}}, angular: {{x: 0.0, y: 0.0, z: {angular}}}}}"
        return self._run(["/cmd_vel"], data, once)

    def emergency_stop(self, active: bool = True):
        """Publish emergency stop flag."""
        data = f"{{data: {str(active).lower()}}}"
        return self._run(["/emergency_stop"], data, once=True)

    def goal_pose(self, x: float, y: float, z: float = 0.0, once: bool = True):
        """Publish a goal pose."""
        data = f"{{header: {{stamp: {{sec: 0, nanosec: 0}}, frame_id: 'map'}}, pose: {{position: {{x: {x}, y: {y}, z: {z}}}, orientation: {{x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}}"
        return self._run(["/goal_pose"], data, once)
