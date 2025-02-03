import linuxcnc

# LinuxCNC stat objektum inicializálása
stat = linuxcnc.stat()

# Gépállapot lekérdezése
def get_machine_status():
    """
    Teljes gépállapot lekérdezése LinuxCNC-ből.
    """
    stat.poll()
    return {
        "state": stat.state,
        "motion_mode": stat.motion_mode,
        "interp_state": stat.interp_state,
        "enabled": stat.enabled,
        "homed": list(stat.homed),
        "estop": stat.estop,
        "active_g_codes": list(stat.active_g_codes),
        "active_m_codes": list(stat.active_m_codes),
        "queue": stat.queue,
        "spindle_speed": stat.spindle_speed,
        "spindle_direction": stat.spindle_direction,
        "feedrate": stat.feedrate,
        "velocity": stat.velocity,
        "dtg": list(stat.dtg),
        "commanded_position": list(stat.position),
        "actual_position": list(stat.actual_position),
        "joint_position": list(stat.joint_position),
        "tool_in_spindle": stat.tool_in_spindle,
        "task_mode": stat.task_mode,
        "task_state": stat.task_state,
        "inputs": list(stat.inputs),
        "outputs": list(stat.outputs),
        "analog_inputs": list(stat.analog_inputs),
        "analog_outputs": list(stat.analog_outputs)
    }

# Egy adott csukló (joint) pozíciójának lekérdezése
def get_joint_position(joint: int):
    """
    Egy adott csukló pozíciójának lekérdezése LinuxCNC-ből.
    """
    stat.poll()
    return {"joint": joint, "position": stat.joint_position[joint]}

# Összes csukló (joint) pozíciójának lekérdezése
def get_all_joint_positions():
    """
    Az összes csukló pozíciójának lekérdezése LinuxCNC-ből.
    """
    stat.poll()
    return {f"joint_{i}": pos for i, pos in enumerate(stat.joint_position)}

# Jelenlegi mozgási mód lekérdezése
def get_motion_mode():
    """
    A jelenlegi mozgási mód lekérdezése LinuxCNC-ből.
    """
    stat.poll()
    return stat.motion_mode
