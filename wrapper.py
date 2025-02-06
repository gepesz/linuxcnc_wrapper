from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.status_service import *
from services.command_service import *
from services.error_service import *
import asyncio
import logging

# Logger beállítása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("linuxcnc_wrapper")

class GCodeUpload(BaseModel):
    filename: str
    content: str

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

# --- Vészgomb aktiválása/deaktiválása ---
@app.post("/cmd/estop")
async def enable_machine_endpoint():
    try:
        estop()
        return json_response("estop", "activated")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("enable_machine", "failed", error=str(e)))

@app.post("/cmd/estop_reset")
async def disable_machine_endpoint():
    try:
        estop_reset()
        return json_response("estop", "reset")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("disable_machine", "failed", error=str(e)))


# --- A gép ki- és be kapcsolása  ---
@app.post("/cmd/enable")
async def enable_machine_endpoint():
    try:
        enable_machine()
        return json_response("machine", "ON")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("enable_machine", "failed", error=str(e)))

@app.post("/cmd/disable")
async def disable_machine_endpoint():
    try:
        disable_machine()
        return json_response("machine", "OFF")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("disable_machine", "failed", error=str(e)))


# --- A gép HOME pozicionálása ---
@app.post("/cmd/home/{joint_id}")
async def home_joint_endpoint(joint_id: int):
    try:
        home_joint(joint_id)
        return json_response("home_joint", "success", {"joint_id": joint_id})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_joint", "failed", error=str(e)))

@app.post("/cmd/home_all")
async def home_all_joints_endpoint():
    try:
        home_all_joints()
        return json_response("home_all_joints", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_all_joints", "failed", error=str(e)))

@app.post("/cmd/unhome/{joint_id}")
async def home_joint_endpoint(joint_id: int):
    try:
        unhome_joint(joint_id)
        return json_response("home_joint", "success", {"joint_id": joint_id})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_joint", "failed", error=str(e)))

@app.post("/cmd/unhome_all")
async def home_all_joints_endpoint():
    try:
        unhome_all_joints()
        return json_response("home_all_joints", "success")
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("home_all_joints", "failed", error=str(e)))


# --- A gép mozgatása ---
@app.post("/cmd/move")
async def move_machine_endpoint(x: float, y: float, z: float):
    try:
        await move_machine(x, y, z)
        return json_response("move_machine", "success", {"x": x, "y": y, "z": z})
    except Exception as e:
        return JSONResponse(status_code=500, content=json_response("move_machine", "failed", error=str(e)))


# --- G-code file feltöltése ---
@app.post("/cmd/load_gcode")
async def load_gcode_file(data: GCodeUpload):
    """
    JSON-ben érkező G-kód fájl tartalmat elmenti és betölti LinuxCNC-be.
    """
    try:
        print(f"📩 Beérkező API hívás: {data}")  # 🛠 Debug kiírás
        result = save_and_load_gcode_into_linuxcnc(data.filename, data.content)
        return result

    except Exception as e:
        print(f"❌ API hiba: {str(e)}")  # 🛠 Hiba kiírás
        return JSONResponse(status_code=500, content=json_response("load_gcode", "failed", error=str(e)))

# --- WebSocket Endpoint (Status és Error csoport) ---
@app.websocket("/ws/status/")
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
