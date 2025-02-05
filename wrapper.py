from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from services.status_service import *
from services.command_service import *
from services.error_service import *
import asyncio
import logging

# Logger beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linuxcnc_wrapper")

# FastAPI alkalmazás inicializálása
app = FastAPI(title="LinuxCNC Wrapper", description="A wrapper between LinuxCNC and frontend", version="1.1.0")


# --- Egységes JSON válasz segédfüggvény ---
def json_response(command: str, status: str, payload: dict = None, error: str = None):
    response = {"command": command, "status": status}
    if payload:
        response["payload"] = payload
    if error:
        response["error"] = error
    return response


# --- REST Endpointok (Command csoport) ---
@app.post("/motion/home/{joint_id}")
async def home_joint_endpoint(joint_id: int):
    try:
        home_joint(joint_id)
        return json_response("home_joint", "success", {"joint_id": joint_id})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_joint", "failed", error=str(e)))


@app.post("/motion/home/all")
async def home_all_joints_endpoint():
    try:
        home_all_joints()
        return json_response("home_all_joints", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_all_joints", "failed", error=str(e)))


@app.post("/motion/enable")
async def enable_machine_endpoint():
    try:
        enable_machine()
        return json_response("enable_machine", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("enable_machine", "failed", error=str(e)))


@app.post("/motion/disable")
async def disable_machine_endpoint():
    try:
        disable_machine()
        return json_response("disable_machine", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("disable_machine", "failed", error=str(e)))


@app.post("/motion/move")
async def move_machine_endpoint(x: float, y: float, z: float):
    try:
        await move_machine(x, y, z)
        return json_response("move_machine", "success", {"x": x, "y": y, "z": z})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("move_machine", "failed", error=str(e)))


# --- WebSocket Endpoint (Status és Error csoport) ---
@app.websocket("/ws/status")
async def status_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Küldjük a gép állapotát
            status_data = get_machine_status()
            machine_status = json_response("machine_status", "success", status_data)
            await websocket.send_json(machine_status)

            # Küldjük a hibaállapotokat, ha vannak
            error_status = get_error_status()
            if error_status:
                await websocket.send_json(json_response("error_status", "success", error_status))

            await asyncio.sleep(1)  # 1 másodpercenként frissítünk
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
