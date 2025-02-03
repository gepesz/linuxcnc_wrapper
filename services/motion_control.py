import linuxcnc
import asyncio

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()

# Gép engedélyezése
def enable_machine():
    """
    Engedélyezi a gép működését LinuxCNC-ben.
    """
    cmd.state(linuxcnc.STATE_ON)

# Gép letiltása
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

# Mozgás leállítása
def stop_motion():
    """
    Az összes mozgás azonnali leállítása LinuxCNC-ben.
    """
    cmd.abort()

# Egy adott csukló (joint) folyamatos mozgatása (jogging)
async def jog_joint(joint: int, direction: int, speed: float):
    """
    Egy adott csukló (joint) jog mozgatása LinuxCNC-ben.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.wait_complete()
    jog_dir = linuxcnc.JOG_POS if direction > 0 else linuxcnc.JOG_NEG
    cmd.jog(linuxcnc.JOG_CONTINUOUS, joint, jog_dir, speed)
    await asyncio.sleep(0.1)
    cmd.jog(linuxcnc.JOG_STOP, joint)

