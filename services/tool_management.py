import linuxcnc

# LinuxCNC command objektum inicializálása
cmd = linuxcnc.command()
stat = linuxcnc.stat()

# Szerszámkezelési funkciók
def change_tool(tool_number: int):
    """
    Szerszámcsere végrehajtása.
    :param tool_number: A kívánt szerszám száma.
    """
    cmd.mode(linuxcnc.MODE_MDI)  # Átváltás MDI módra
    cmd.wait_complete()
    cmd.mdi(f"T{tool_number} M6")  # Szerszámcsere parancs
    cmd.wait_complete()

def get_current_tool() -> int:
    """
    Az aktuálisan betöltött szerszám lekérdezése.
    :return: Az aktuális szerszám száma.
    """
    stat.poll()
    return stat.tool_in_spindle

def load_tool_table(tool_table_file: str):
    """
    Szerszámtábla betöltése fájlból.
    :param tool_table_file: A szerszámtábla fájl elérési útja.
    """
    cmd.load_tool_table(tool_table_file)

def set_tool_offset(tool_number: int, length_offset: float, diameter_offset: float):
    """
    Szerszám offsetek beállítása.
    :param tool_number: A szerszám száma.
    :param length_offset: Hossz offset.
    :param diameter_offset: Átmérő offset.
    """
    cmd.set_tool_offset(tool_number, length_offset, diameter_offset)
    cmd.wait_complete()

def clear_tool_offset():
    """
    Az aktuális szerszám offsetek törlése.
    """
    cmd.mdi("G49")  # Szerszámkompenzáció törlése
    cmd.wait_complete()
