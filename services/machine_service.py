import linuxcnc
from models import MachineStatus

# LinuxCNC stat objektum inicializálása
stat = linuxcnc.stat()

# Gép állapot lekérdezési funkciók
def get_machine_status():
    """
    Gépi állapot lekérdezése a LinuxCNC-ből.
    """
    stat.poll()  # Frissíti az állapotot
    return MachineStatus(
        x_position=stat.axis[0]['position'],
        y_position=stat.axis[1]['position'],
        z_position=stat.axis[2]['position'],
        is_running=stat.program_running,
        error_code=stat.error,
        message="No errors" if stat.error == 0 else "Error occurred",
    )

# Tengelyek (axis) és csuklók (joint) állapotainak kezelése
def get_axis_position(axis: int) -> float:
    """
    Egy adott tengely pozíciójának lekérdezése.
    """
    stat.poll()
    return stat.axis[axis]['position']

def get_joint_position(joint: int) -> float:
    """
    Egy adott csukló pozíciójának lekérdezése.
    """
    stat.poll()
    return stat.joint[joint]['position']

def get_all_axes_positions() -> dict:
    """
    Az összes tengely pozíciójának lekérdezése.
    """
    stat.poll()
    return {f"axis_{i}": axis['position'] for i, axis in enumerate(stat.axis)}

def get_all_joints_positions() -> dict:
    """
    Az összes csukló pozíciójának lekérdezése.
    """
    stat.poll()
    return {f"joint_{i}": joint['position'] for i, joint in enumerate(stat.joint)}

def get_joint_following_errors() -> dict:
    """
    Az összes csukló követési hibájának lekérdezése.
    """
    stat.poll()
    return {f"joint_{i}": joint['following_error'] for i, joint in enumerate(stat.joint)}

# Mozgásvezérlés módok és aktív kódok
def get_motion_mode() -> str:
    """
    Jelenlegi mozgási mód lekérdezése.
    """
    stat.poll()
    return stat.motion_mode

def get_active_codes() -> dict:
    """
    Aktív G és M kódok lekérdezése.
    """
    stat.poll()
    return {
        "g_codes": stat.active_g_codes,
        "m_codes": stat.active_m_codes,
    }

# Gépvezérlési állapotok
def is_estop_active() -> bool:
    """
    Ellenőrzi, hogy a vészleállítás aktív-e.
    """
    stat.poll()
    return stat.estop

def is_machine_enabled() -> bool:
    """
    Ellenőrzi, hogy a gépvezérlés engedélyezett-e.
    """
    stat.poll()
    return stat.enabled

def is_homed() -> bool:
    """
    Ellenőrzi, hogy az összes csukló home állapotban van-e.
    """
    stat.poll()
    return all(joint['homed'] for joint in stat.joint)

def is_program_running() -> bool:
    """
    Ellenőrzi, hogy a program fut-e.
    """
    stat.poll()
    return stat.program_running

def is_program_paused() -> bool:
    """
    Ellenőrzi, hogy a program szünetel-e.
    """
    stat.poll()
    return stat.program_paused

def get_current_line() -> int:
    """
    Az aktuálisan futó G-kód sorának száma.
    """
    stat.poll()
    return stat.current_line

# Előtolási és fordulatszám paraméterek
def get_feed_rate() -> float:
    """
    Az aktuális előtolási sebesség lekérdezése.
    """
    stat.poll()
    return stat.feedrate

def get_spindle_speed() -> float:
    """
    Az aktuális orsófordulatszám lekérdezése.
    """
    stat.poll()
    return stat.spindle[0]['speed'] if len(stat.spindle) > 0 and 'speed' in stat.spindle[0] else 0.0

def get_spindle_direction() -> str:
    """
    Az orsó forgásirányának lekérdezése.
    """
    stat.poll()
    return stat.spindle[0]['direction'] if len(stat.spindle) > 0 and 'direction' in stat.spindle[0] else "unknown"
