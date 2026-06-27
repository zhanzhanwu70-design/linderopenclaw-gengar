"""Robot state management for ELLE AMR."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional
from geometry_msgs.msg import Pose


class RobotMode(Enum):
    IDLE = "idle"
    SIMULATION = "simulation"
    MAPPING = "mapping"
    LOCALIZATION = "localization"
    NAVIGATION = "navigation"


class NavigationStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class NodeOverallStatus(Enum):
    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"


class BtNodeStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class SimulationState:
    running: bool = False
    world_name: str = "DefaultWorld"
    robot_model: str = "elle_robox500_1"


@dataclass
class MappingState:
    active: bool = False
    method: str = "slam_toolbox"  # or cartographer
    map_saved: bool = False
    map_path: Optional[str] = None


@dataclass
class LocalizationState:
    active: bool = False
    map_loaded: bool = False


@dataclass
class NavigationState:
    active: bool = False
    current_goal: Optional[Pose] = None
    status: NavigationStatus = NavigationStatus.IDLE


@dataclass
class SensorStatus:
    name: str
    status: str  # ok, warning, error
    value: float = 0.0


@dataclass
class NodeStatus:
    name: str
    status: NodeOverallStatus
    error_code: str = ""


@dataclass
class BtStatus:
    current_node: str = ""
    status: BtNodeStatus = BtNodeStatus.IDLE
    message: str = ""


@dataclass
class RobotStatus:
    battery_level: float = 100.0
    emergency_stop: bool = False
    sensors: Dict[str, SensorStatus] = field(default_factory=dict)
    nodes: Dict[str, NodeStatus] = field(default_factory=dict)
    bt_status: BtStatus = field(default_factory=BtStatus)


@dataclass
class ElleAgentState:
    mode: RobotMode = RobotMode.IDLE
    simulation: SimulationState = field(default_factory=SimulationState)
    mapping: MappingState = field(default_factory=MappingState)
    localization: LocalizationState = field(default_factory=LocalizationState)
    navigation: NavigationState = field(default_factory=NavigationState)
    robot_status: RobotStatus = field(default_factory=RobotStatus)

    # Supported robot models
    SUPPORTED_MODELS = [
        "elle_robox500_1",
        "teco_ust100_1",
        "noveltek_robox300_1",
        "wheeltec_aie510_1",
        "scuttle_capa55r_1",
        "nexus_robox300_1",
        "custom_1",
    ]

    def set_mode(self, mode: RobotMode):
        self.mode = mode

    def is_safe(self) -> bool:
        """Check if robot is in a safe state."""
        if self.robot_status.emergency_stop:
            return False
        if self.mode == RobotMode.NAVIGATION:
            return self.navigation.status not in [
                NavigationStatus.FAILED
            ]
        return True

    def summary(self) -> str:
        return (
            f"Mode: {self.mode.value} | "
            f"Sim: {self.simulation.running} | "
            f"Map: {self.mapping.active} | "
            f"Nav: {self.navigation.status.value} | "
            f"E-Stop: {self.robot_status.emergency_stop}"
        )
