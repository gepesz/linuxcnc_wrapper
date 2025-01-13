import linuxcnc
import asyncio

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()

# Mozgásvezérlési funkciók
def enable_machine():
    """
    Engedélyezi a gépvezérlést.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)  # Mód váltás kézi vezérlésre
    cmd.wait_complete()  # Vár, amíg a módváltás befejeződik
    cmd.machine_on()

def disable_machine():
    """
    Letiltja a gépvezérlést.
    """
    cmd.machine_off()

async def move_machine(x: float, y: float, z: float):
    """
    A gép mozgatása a megadott pozíciókra.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)  # Átállítás kézi módba
    cmd.wait_complete()  # Várakozás a beállítás befejezésére
    cmd.jog(linuxcnc.JOG_CONTINUOUS, 0, x)  # X tengely mozgatása
    cmd.jog(linuxcnc.JOG_CONTINUOUS, 1, y)  # Y tengely mozgatása
    cmd.jog(linuxcnc.JOG_CONTINUOUS, 2, z)  # Z tengely mozgatása
    await asyncio.sleep(1)  # Szimulált mozgási idő
    cmd.abort()  # Mozgás leállítása
    return {"status": "Machine moved", "x": x, "y": y, "z": z}

def home_axis(axis: int):
    """
    Egy adott tengely nullázása (home).
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.wait_complete()
    cmd.home(axis)
    cmd.wait_complete()

def home_all_axes():
    """
    Az összes tengely nullázása (home).
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.wait_complete()
    cmd.home(-1)  # -1 jelenti az összes tengelyt
    cmd.wait_complete()

def stop_motion():
    """
    Mozgás leállítása.
    """
    cmd.abort()

async def jog_axis(axis: int, direction: int, speed: float):
    """
    Egy adott tengely folyamatos mozgatása (jogging).
    :param axis: A tengely indexe.
    :param direction: Mozgás iránya (-1: negatív, 1: pozitív).
    :param speed: Mozgás sebessége.
    """
    cmd.mode(linuxcnc.MODE_MANUAL)
    cmd.wait_complete()
    cmd.jog(linuxcnc.JOG_CONTINUOUS, axis, direction * speed)
    await asyncio.sleep(1)  # Szimulációs idő, amíg a mozgás zajlik
    cmd.jog(linuxcnc.JOG_STOP, axis)  # Mozgás megállítása
