from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
from services.machine_service import (
    get_machine_status,
    get_axis_position,
    get_joint_position,
    get_all_axes_positions,
    get_all_joints_positions,
    get_motion_mode,
)
from services.motion_control import (
    enable_machine,
    disable_machine,
    move_machine,
    home_axis,
    home_all_axes,
    stop_motion,
    jog_axis,
)
import asyncio

# FastAPI alkalmazás inicializálása
app = FastAPI(title="LinuxCNC Wrapper", description="A wrapper between LinuxCNC and frontend", version="1.0.0")

# --- REST Endpointok ---
@app.get("/status")
async def status_endpoint():
    """
    Gép állapotának lekérdezése.
    """
    return get_machine_status()

@app.get("/axis/{axis_id}/position")
async def axis_position_endpoint(axis_id: int):
    """
    Egy adott tengely pozíciójának lekérdezése.
    """
    return {"axis": axis_id, "position": get_axis_position(axis_id)}

@app.get("/joint/{joint_id}/position")
async def joint_position_endpoint(joint_id: int):
    """
    Egy adott csukló pozíciójának lekérdezése.
    """
    return {"joint": joint_id, "position": get_joint_position(joint_id)}

@app.post("/motion/enable")
async def enable_machine_endpoint():
    """
    A gépvezérlés engedélyezése.
    """
    enable_machine()
    return {"status": "Machine enabled"}

@app.post("/motion/disable")
async def disable_machine_endpoint():
    """
    A gépvezérlés letiltása.
    """
    disable_machine()
    return {"status": "Machine disabled"}

@app.post("/motion/move")
async def move_machine_endpoint(x: float, y: float, z: float):
    """
    A gép mozgatása a megadott pozíciókra.
    """
    return await move_machine(x, y, z)

@app.post("/motion/home/{axis_id}")
async def home_axis_endpoint(axis_id: int):
    """
    Egy adott tengely nullázása.
    """
    home_axis(axis_id)
    return {"status": f"Axis {axis_id} homed"}

@app.post("/motion/home/all")
async def home_all_axes_endpoint():
    """
    Az összes tengely nullázása.
    """
    home_all_axes()
    return {"status": "All axes homed"}

@app.post("/motion/stop")
async def stop_motion_endpoint():
    """
    Mozgás leállítása.
    """
    stop_motion()
    return {"status": "Motion stopped"}

@app.post("/motion/jog")
async def jog_axis_endpoint(axis: int, direction: int, speed: float):
    """
    Egy tengely folyamatos mozgatása.
    """
    await jog_axis(axis, direction, speed)
    return {"status": f"Axis {axis} jogged in direction {direction} at speed {speed}"}

# --- WebSocket Endpoint ---
@app.websocket("/ws/status")
async def status_websocket(websocket: WebSocket):
    """
    Valós idejű állapotfrissítések WebSocket-en keresztül.
    """
    await websocket.accept()
    try:
        while True:
            websocket_data = {
                "machine_status": get_machine_status(),
                "motion_mode": get_motion_mode(),
            }
            await websocket.send_json(websocket_data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket connection closed")


