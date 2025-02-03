from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from services.machine_service import *
from services.motion_control import *
import asyncio
import logging
import linuxcnc

# Logger beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linuxcnc_wrapper")

# FastAPI alkalmazás inicializálása
app = FastAPI(title="LinuxCNC Wrapper", description="A wrapper between LinuxCNC and frontend", version="1.0.0")

# --- Egységes válaszsegítő függvény ---
def json_response(type_: str, command: str, status: str, payload: dict = None, error: str = None):
    response = {"type": type_, "command": command, "status": status}
    if payload:
        response["payload"] = payload
    if error:
        response["error"] = error
    return response

# --- REST Endpointok ---
@app.get("/status")
async def status_endpoint():
    try:
        status = get_machine_status()
        return json_response("response", "get_machine_status", "success", {"status": status})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "get_machine_status", "failed", error=str(e)))

@app.get("/status/full")
async def full_status_endpoint():
    try:
        stat = linuxcnc.stat()
        stat.poll()
        full_status = {attr: getattr(stat, attr) for attr in dir(stat) if not attr.startswith("_") and callable(getattr(stat, attr)) is False}
        return json_response("response", "get_full_linuxcnc_status", "success", {"full_status": full_status})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "get_full_linuxcnc_status", "failed", error=str(e)))

@app.get("/joint/{joint_id}/position")
async def joint_position_endpoint(joint_id: int):
    try:
        position = get_joint_position(joint_id)
        return json_response("response", "get_axis_position", "success", {"axis": joint_id, "position": position})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "get_axis_position", "failed", error=str(e)))

@app.post("/motion/enable")
async def enable_machine_endpoint():
    try:
        enable_machine()
        return json_response("response", "enable_machine", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "enable_machine", "failed", error=str(e)))

@app.post("/motion/disable")
async def disable_machine_endpoint():
    try:
        disable_machine()
        return json_response("response", "disable_machine", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "disable_machine", "failed", error=str(e)))

@app.post("/motion/move")
async def move_machine_endpoint(x: float, y: float, z: float):
    try:
        await move_machine(x, y, z)
        return json_response("response", "move_machine", "in_progress", {"x": x, "y": y, "z": z})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "move_machine", "failed", error=str(e)))

@app.post("/motion/home/{joint_id}")
async def home_joint_endpoint(joint_id: int):
    try:
        home_joint(joint_id)
        return json_response("response", "home_axis", "success", {"axis": joint_id})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "home_axis", "failed", error=str(e)))

@app.post("/motion/home/all")
async def home_all_joints_endpoint():
    try:
        home_all_joints()
        return json_response("response", "home_all_axes", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "home_all_axes", "failed", error=str(e)))

@app.post("/motion/stop")
async def stop_motion_endpoint():
    try:
        stop_motion()
        return json_response("response", "stop_motion", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "stop_motion", "failed", error=str(e)))

@app.post("/motion/jog")
async def jog_joint_endpoint(joint: int, direction: int, speed: float):
    try:
        await jog_joint(joint, direction, speed)
        return json_response("response", "jog_joint", "success", {"joint": joint, "direction": direction, "speed": speed})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("error", "jog_joint", "failed", error=str(e)))

# --- WebSocket Endpoint ---
@app.websocket("/ws/status")
async def status_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Bejövő parancsok kezelése
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.1)
                command = data.get("command")
                parameters = data.get("parameters", {})

                response = handle_websocket_command(command, parameters)
                await websocket.send_json(response)
            except asyncio.TimeoutError:
                pass  # Ha nincs bejövő üzenet, csak küldjük az állapotot

            # Gép állapotának küldése
            websocket_data = json_response("event", "machine_status", "success", {
                "machine_status": get_machine_status(),
                "motion_mode": get_motion_mode(),
                "joints_position": get_all_joint_positions()
            })
            await websocket.send_json(websocket_data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")

# WebSocket parancsok kezelése
def handle_websocket_command(command: str, parameters: dict):
    try:
        if command == "enable_machine":
            enable_machine()
            return json_response("response", command, "success")

        if command == "disable_machine":
            disable_machine()
            return json_response("response", command, "success")

        if command == "move":
            x = parameters.get("x", 0)
            y = parameters.get("y", 0)
            z = parameters.get("z", 0)
            asyncio.create_task(move_machine(x, y, z))
            return json_response("response", command, "in_progress", {"x": x, "y": y, "z": z})

        return json_response("error", command, "failed", error="Unknown command")
    except Exception as e:
        return json_response("error", command, "failed", error=str(e))
