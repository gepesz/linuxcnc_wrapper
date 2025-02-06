import os
import linuxcnc
import asyncio

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()
stat = linuxcnc.stat()

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
    Egy adott csukló (joint) home pozíciójának törlése LinuxCNC-ben.
    """
    try:
        stat.poll()
        # Ha a gép nincs joint módban, állítsuk be
        if stat.task_mode != linuxcnc.MODE_MANUAL:
            print("🔄 Átváltás joint módba...")
            cmd.mode(linuxcnc.MODE_MANUAL)
            cmd.wait_complete()

        # Ha a gép nincs letiltva, tiltsuk le az unhome előtt
        if not stat.enabled:
            print("🛑 A gép letiltása az unhome előtt...")
            cmd.state(linuxcnc.STATE_OFF)
            cmd.wait_complete()

        # Most már küldhetjük az unhome parancsot
        print(f"🔄 Unhome joint {joint_id}...")
        cmd.unhome(joint_id)
        cmd.wait_complete()
        cmd.state(linuxcnc.STATE_ON)

        return {"command": "unhome", "status": "success", "message": f"Joint {joint_id} unhomed."}

    except Exception as e:
        return {"command": "unhome", "status": "failed", "error": str(e)}



# Összes csukló nullázásának visszavonása
def unhome_all_joints():
    """
    Az összes csukló (joint) home pozíciójának törlése LinuxCNC-ben.
    """
    try:
        stat.poll()
        # Ha a gép nincs joint módban, állítsuk be
        if stat.task_mode != linuxcnc.MODE_MANUAL:
            print("🔄 Átváltás joint módba...")
            cmd.mode(linuxcnc.MODE_MANUAL)
            cmd.wait_complete()

        # Ha a gép nincs letiltva, tiltsuk le az unhome előtt
        if not stat.enabled:
            print("🛑 A gép letiltása az unhome előtt...")
            cmd.state(linuxcnc.STATE_OFF)
            cmd.wait_complete()

        # Most már küldhetjük az unhome parancsot
        print(f"🔄 Unhome az összes csuklóra...")
        cmd.unhome(-1)
        cmd.wait_complete()
        cmd.state(linuxcnc.STATE_ON)

        return {"command": "unhome_all", "status": "success", "message": "All joint unhomed"}

    except Exception as e:
        return {"command": "unhome_all", "status": "failed", "error": str(e)}


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