import linuxcnc
import asyncio

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()

# Gép engedélyezése
def estop():
    """
    Engedélyezi a gép működését LinuxCNC-ben.
    """
    cmd.state(linuxcnc.STATE_ESTOP)

# Gép letiltása
def estop_reset():
    """
    Letiltja a gép működését LinuxCNC-ben.
    """
    cmd.state(linuxcnc.STATE_ESTOP_RESET)

# Gép bekapcsolása
def enable_machine():
    """
    Engedélyezi a gép működését LinuxCNC-ben.
    """
    cmd.state(linuxcnc.STATE_ON)

# Gép kikapcsolása
def disable_machine():
    """
    Letiltja a gép működését LinuxCNC-ben.
    """
    cmd.state(linuxcnc.STATE_OFF)

# Mozgás végrehajtása adott koordinátákra
async def move_machine(x: float, y: float, z: float):
    """
    A gép mozgatása a megadott koordinátákra LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MDI)
    cmd.wait_complete()
    cmd.mdi(f"G0 X{x} Y{y} Z{z}")
    await asyncio.sleep(0.1)

# Egy adott csukló (joint) nullázása
def home_joint(joint_id: int):
    """
    Egy adott csukló (joint) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.home(joint_id)

# Összes csukló nullázása
def home_all_joints():
    """
    Az összes csukló (joint) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.home(-1)

# Egy adott csukló (joint) nullázásának visszavonása
def unhome_joint(joint_id: int):
    """
    Egy adott csukló (joint) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.unhome(joint_id)

# Összes csukló nullázásának visszavonása
def unhome_all_joints():
    """
    Az összes csukló (joint) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.unhome(-1)

# Mozgás leállítása
def stop_motion():
    """
    Leállítja a folyamatban lévő mozgást.
    """
    cmd.abort()

# Egy adott csukló (joint) mozgatása (jog)
async def jog_joint(joint: int, direction: int, speed: float):
    """
    Egy adott csukló mozgatása megadott irányba és sebességgel.
    """
    cmd.mode (linuxcnc.MODE_MANUAL)
    cmd.wait_complete()
    jog_dir = 1 if direction > 0 else -1
    cmd.jog(linuxcnc.JOG_CONTINUOUS, True, joint, direction * speed)
    await asyncio.sleep(0.1)
    cmd.jog(linuxcnc.JOG_STOP, True, joint, 0)

# G-kód fájl betöltése
def load_gcode_into_linuxcnc(file_name: str, content: str):
    """
    Betölt egy G-kód fájlt a LinuxCNC-be.
    """
    try:
        with open(file_name, "w") as file:
            file.write(content)
        cmd.program_open(file_name)
        return {"command": "load_gcode", "status": "success", "message": f"File {file_name} loaded into LinuxCNC."}

    except Exception as e:
        return {"command": "load_gcode", "status": "failed", "error": str(e)}
