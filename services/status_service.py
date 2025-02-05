import linuxcnc

# LinuxCNC stat objektum inicializálása
stat = linuxcnc.stat()

# Gép állapotának lekérdezése
def get_machine_status():
    """
    Visszaadja a gép aktuális állapotát.
    """
    stat.poll()
    return {
        "state": stat.state,
        "motion_mode": stat.motion_mode,
        "interp_state": stat.interp_state,
        "enabled": stat.enabled,
        "homed": list(stat.homed),
        "estop": stat.estop,
        "queue": stat.queue,
        "feedrate": stat.feedrate,
        "velocity": stat.velocity,
        "dtg": list(stat.dtg),
        "commanded_position": list(stat.position),
        "actual_position": list(stat.actual_position),
        "joint_position": list(stat.joint_position),
        "tool_in_spindle": stat.tool_in_spindle,
        "task_mode": stat.task_mode,
    }

# Összes csukló pozíciójának lekérdezése
def get_all_joint_positions():
    """
    Visszaadja az összes csukló pillanatnyi pozícióját.
    """
    stat.poll()
    return list(stat.joint_position)

# Mozgási mód lekérdezése
def get_motion_mode():
    """
    Visszaadja a mozgási módot.
    """
    stat.poll()
    return stat.motion_mode
