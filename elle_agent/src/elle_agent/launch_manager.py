"""Launch file orchestration for ELLE_WS.

Operates the robot primarily through tested launch configurations,
delegating complex component composition to existing launch files.
"""

import subprocess
import time
from typing import Dict, List, Optional, Tuple

from .state import ElleAgentState, RobotMode


# ROS2 workspace paths
ELLE_WS = "/home/node/elle_ws"  # symlink to actual workspace
ROS_SETUP = "/opt/ros/humble/setup.bash"
WS_SETUP = f"{ELLE_WS}/install/local_setup.bash"


class LaunchManager:
    """Manages ROS2 launch processes for ELLE_WS."""

    def __init__(self, state: ElleAgentState):
        self.state = state
        self.processes: Dict[str, subprocess.Popen] = {}

    def _run_launch(
        self,
        package: str,
        launch_file: str,
        args: Optional[List[str]] = None,
        timeout: int = 30,
    ) -> Tuple[int, str, str]:
        """Run a ros2 launch command and return (returncode, stdout, stderr)."""
        cmd = [
            "bash", "-c",
            f"source {ROS_SETUP} && source {WS_SETUP} && "
            f"ros2 launch {package} {launch_file} " + " ".join(args or [])
        ]
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr

    def start_process(
        self,
        name: str,
        package: str,
        launch_file: str,
        args: Optional[List[str]] = None,
    ) -> bool:
        """Start a launch file as a background process."""
        if name in self.processes:
            return False  # already running

        cmd = [
            "bash", "-c",
            f"source {ROS_SETUP} && source {WS_SETUP} && "
            f"ros2 launch {package} {launch_file} " + " ".join(args or [])
        ]
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.processes[name] = proc
            return True
        except Exception:
            return False

    def stop_process(self, name: str) -> bool:
        """Stop a named launch process."""
        if name not in self.processes:
            return False
        proc = self.processes[name]
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        del self.processes[name]
        return True

    def stop_all(self):
        """Stop all launch processes."""
        for name in list(self.processes.keys()):
            self.stop_process(name)

    # ─── Simulation ────────────────────────────────────────────

    def start_simulation(
        self,
        world_name: str = "DefaultWorld",
        robot_model: Optional[str] = None,
        use_gz_gui: bool = True,
    ) -> bool:
        """Start Gazebo simulation world with robot."""
        if self.state.simulation.running:
            return False

        model = robot_model or self.state.simulation.robot_model
        args = [
            f"robot_model:={model}",
            f"world_name:={world_name}",
            f"use_gz_gui:={str(use_gz_gui).lower()}",
            "use_sim_time:=true",
        ]
        ok = self.start_process(
            "simulation",
            "elle_simulations",
            "world.launch.py",
            args,
        )
        if ok:
            self.state.simulation.running = True
            self.state.simulation.world_name = world_name
            self.state.simulation.robot_model = model
            self.state.set_mode(RobotMode.SIMULATION)
        return ok

    def stop_simulation(self) -> bool:
        """Stop simulation and kill Gazebo processes."""
        ok = self.stop_process("simulation")
        # Also kill any orphan gz processes
        subprocess.run(["pkill", "-f", "gz sim"], capture_output=True)
        self.state.simulation.running = False
        if self.state.mode == RobotMode.SIMULATION:
            self.state.set_mode(RobotMode.IDLE)
        return ok

    # ─── SLAM / Mapping ────────────────────────────────────────

    def start_slam(
        self,
        method: str = "slam_toolbox",
        open_rviz: bool = False,
    ) -> bool:
        """Start SLAM mapping."""
        if self.state.mapping.active:
            return False

        slam_pkg = "slam" if method == "slam_toolbox" else "cartographer"
        args = [
            f"open_rviz:={str(open_rviz).lower()}",
            "use_sim_time:=true",
        ]
        ok = self.start_process(
            "slam",
            "slam",
            "online_async_launch.py" if method == "slam_toolbox" else "launch.py",
            args,
        )
        if ok:
            self.state.mapping.active = True
            self.state.mapping.method = method
            self.state.set_mode(RobotMode.MAPPING)
        return ok

    def stop_slam(self) -> bool:
        """Stop SLAM mapping."""
        ok = self.stop_process("slam")
        self.state.mapping.active = False
        if self.state.mode == RobotMode.MAPPING:
            self.state.set_mode(RobotMode.IDLE)
        return ok

    # ─── Localization ─────────────────────────────────────────

    def start_localization(
        self,
        map_path: Optional[str] = None,
        params_file: Optional[str] = None,
        open_rviz: bool = False,
    ) -> bool:
        """Start AMCL localization with a map."""
        if self.state.localization.active:
            return False

        args = []
        if map_path:
            args.append(f"map:={map_path}")
        if params_file:
            args.append(f"params_file:={params_file}")
        args.append(f"open_rviz:={str(open_rviz).lower()}")
        args.append("use_sim_time:=true")

        ok = self.start_process(
            "localization",
            "navigation2",
            "localization_launch.py",
            args,
        )
        if ok:
            self.state.localization.active = True
            self.state.localization.map_loaded = map_path is not None
            self.state.set_mode(RobotMode.LOCALIZATION)
        return ok

    def stop_localization(self) -> bool:
        """Stop AMCL localization."""
        ok = self.stop_process("localization")
        self.state.localization.active = False
        if self.state.mode == RobotMode.LOCALIZATION:
            self.state.set_mode(RobotMode.IDLE)
        return ok

    # ─── Navigation ────────────────────────────────────────────

    def start_navigation(
        self,
        params_file: Optional[str] = None,
        namespace: str = "",
        autostart: bool = True,
    ) -> bool:
        """Start full Nav2 navigation stack."""
        if self.state.navigation.active:
            return False

        args = [
            f"namespace:={namespace}",
            f"autostart:={str(autostart).lower()}",
            "use_sim_time:=true",
        ]
        if params_file:
            args.append(f"params_file:={params_file}")

        ok = self.start_process(
            "navigation",
            "navigation2",
            "bringup_launch.py",
            args,
        )
        if ok:
            self.state.navigation.active = True
            self.state.set_mode(RobotMode.NAVIGATION)
        return ok

    def stop_navigation(self) -> bool:
        """Stop navigation stack."""
        ok = self.stop_process("navigation")
        self.state.navigation.active = False
        self.state.navigation.status = "idle"
        if self.state.mode == RobotMode.NAVIGATION:
            self.state.set_mode(RobotMode.IDLE)
        return ok

    # ─── Bringup ────────────────────────────────────────────────

    def start_bringup(
        self,
        robot_model: Optional[str] = None,
        use_sim_time: bool = True,
    ) -> bool:
        """Start full robot bringup (middleware + coordinator)."""
        model = robot_model or self.state.simulation.robot_model
        args = [
            f"robot_model:={model}",
            f"use_sim_time:={str(use_sim_time).lower()}",
        ]
        return self.start_process("bringup", "bringup", "bringup.launch.py", args)

    def stop_bringup(self) -> bool:
        """Stop robot bringup."""
        return self.stop_process("bringup")

    # ─── Status ─────────────────────────────────────────────────

    def is_running(self, name: str) -> bool:
        """Check if a named process is still running."""
        if name not in self.processes:
            return False
        return self.processes[name].poll() is None

    def status(self) -> Dict[str, bool]:
        """Return status of all managed processes."""
        return {name: self.is_running(name) for name in self.processes}
