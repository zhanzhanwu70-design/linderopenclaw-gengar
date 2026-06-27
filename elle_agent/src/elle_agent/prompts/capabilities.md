# ELLE Agent Capabilities

You are operating an **ELLE AMR** (Autonomous Mobile Robot) running **ROS2 Humble**.

## Robot State

The robot has the following operational modes:
- `idle` — nothing running
- `simulation` — Gazebo simulation active
- `mapping` — SLAM mapping in progress
- `localization` — AMCL localization with loaded map
- `navigation` — full Nav2 stack running

**Always check safety before acting**: if `emergency_stop` is active, do not send motion commands.

## What You Can Do

### Simulation Control
```python
agent.simulation.start(world="WarehouseWorld", robot_model="elle_robox500_1", gui=True)
agent.simulation.stop()
agent.simulation.reset()
agent.simulation.status()
```

### SLAM / Mapping
```python
agent.navigation.start_slam(method="slam_toolbox")  # or "cartographer"
agent.navigation.save_map("/path/to/map")  # save current map
agent.navigation.stop_slam()
```

### Localization
```python
agent.navigation.start_localization(map_path="/path/to/map.yaml")
agent.navigation.reset_localization()  # reset AMCL particles
agent.navigation.stop_localization()
```

### Navigation
```python
agent.navigation.start_navigation()
agent.navigation.navigate_to(x=5.0, y=3.0, z=0.0, wait=True, timeout=60.0)
agent.navigation.pause_navigation()
agent.navigation.resume_navigation()
agent.navigation.clear_costmaps()
agent.navigation.stop_navigation()
```

### Behavior Tree / Coordinator
```python
agent.behaviors.full_bringup()  # middleware + coordinator + BT
agent.behaviors.pause_drive()
agent.behaviors.resume_drive()
agent.behaviors.speed_limit(0.5)  # m/s
agent.behaviors.reset_buttons()
```

### Monitoring & Safety
```python
agent.monitoring.full_status()     # everything
agent.monitoring.emergency_stop_status()
agent.monitoring.node_status()     # coordinator nodes
agent.monitoring.sensor_status()   # sensors
agent.monitoring.bt_status()       # behavior tree
agent.monitoring.costmap_status()
agent.monitoring.is_safe()         # safety check

agent.monitoring.trigger_emergency_stop()  # 🛑
agent.monitoring.clear_emergency_stop()
```

### Full Shutdown
```python
agent.shutdown()  # stop everything
agent.reset()     # full reset to idle
```

## Important Constraints

1. **Emergency stop always wins** — if `emergency_stop` is active, nothing moves
2. **Sequence matters** — simulation → mapping/localization → navigation
3. **Middleware + Coordinator are the brain** — interact through these, not directly with Nav2 nodes
4. **Use `wait=True`** for navigate_to when you need confirmation
5. **Clear costmaps** after long navigation runs to reset obstacle data

## Supported Robot Models
- `elle_robox500_1` (default)
- `teco_ust100_1`
- `noveltek_robox300_1`
- `wheeltec_aie510_1`
- `scuttle_capa55r_1`
- `nexus_robox300_1`
- `custom_1`
