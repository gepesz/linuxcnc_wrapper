import os
import linuxcnc
import asyncio

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()
stat = linuxcnc.stat()

axis_to_joint = {
    "x": [0],
    "y": [1,2],
    "z": [3]
}

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

# Egy adott tengely (axis) nullázása
def home_joint(axis: str):
    """
    Egy adott tengely (axis)  csuklóinak (joints) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.teleop_enable(0)
    joints = axis_to_joint.get(axis, [])
    for joint_id in joints:
        cmd.home(joint_id)

# Összes csukló nullázása
def home_all_joints():
    """
    Az összes csukló (joint) home pozícióba állítása LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.teleop_enable(0)
    cmd.home(-1)

# Egy adott csukló (joint) nullázásának visszavonása
def unhome_joint(axis: str):
    """
    Egy adott csukló (joint) home pozíciójának törlése LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.teleop_enable(0)
    joints = axis_to_joint.get(axis, [])
    for joint_id in joints:
        cmd.unhome(joint_id)

# Összes csukló nullázásának visszavonása
def unhome_all_joints():
    """
    Az összes csukló (joint) home pozíciójának törlése LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.teleop_enable(0)
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
    cmd.jog(linuxcnc.JOG_CONTINUOUS, True, joint, jog_dir * speed)
    await asyncio.sleep(0.1)
    cmd.jog(linuxcnc.JOG_STOP, True, joint, 0)

# G-kód fájl betöltése
def save_and_load_gcode_into_linuxcnc(filename: str, content: str):
    """
    G-kód elmentése fájlba és betöltése LinuxCNC-be.
    """
    LINUXCNC_GCODE_PATH = "/home/cnc/linuxcnc/nc_files"
    try:
        file_path = os.path.join(LINUXCNC_GCODE_PATH, filename)
        print(f"📂 Fájl mentése: {file_path}")  # 🛠 Debug kiírás

        with open(file_path, "w") as file:
            file.write(content)

        print(f"📥 Betöltés LinuxCNC-be: {file_path}")  # 🛠 Debug kiírás
        c = linuxcnc.command()
        c.program_open(file_path)

        return {"command": "load_gcode", "status": "success", "message": f"File {filename} saved and loaded into LinuxCNC."}

    except Exception as e:
        print(f"❌ Hiba LinuxCNC betöltésnél: {str(e)}")  # 🛠 Debug kiírás
        return {"command": "load_gcode", "status": "failed", "error": str(e)}