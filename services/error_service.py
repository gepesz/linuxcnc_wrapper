import linuxcnc

# LinuxCNC stat objektum inicializálása
stat = linuxcnc.stat()
error_channel = linuxcnc.error_channel()


# Hibák lekérdezése
def get_error_status():
    """
    Visszaadja az aktuális hibaállapotokat, beleértve az error channel felől érkező hibákat.
    """
    stat.poll()

    errors = {
        "misc_error": stat.misc_error if hasattr(stat, 'misc_error') else [],
        "interpreter_errcode": stat.interpreter_errcode if hasattr(stat, 'interpreter_errcode') else None,
        "estop": stat.estop,
        "joint_faults": [joint.get("fault", 0) for joint in getattr(stat, "joint", [])],
        "spindle_faults": [spindle.get("orient_fault", 0) for spindle in getattr(stat, "spindle", [])],
        "error_messages": []
    }

    # Error channel feldolgozása
    error = error_channel.poll()
    if error:
        kind, text = error
        if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
            error_type = "error"
        else:
            error_type = "info"
        errors["error_messages"].append({"type": error_type, "message": text})

    return errors
