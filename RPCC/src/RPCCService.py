import datetime
import socket
import fastapi

from rich import print

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


HOST = socket.gethostname()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def execute(command: str) -> dict:
    print(f"Execute '{command}'")
    return {
        "exitcode": "-42",
        "stdout": None
        }

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app = fastapi.FastAPI()
app.title = "Raspberry Pi Command & Control"
app.description = "Remote functions for a raspberry pi which can be called with url's."
app.version = "1.0"
app.contact = {
    "name": "ObiWanLansi",
    "url": "https://github.com/ObiWanLansi/OWLSTB/tree/main/RPCC"
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/status", summary="Return the current status of the server.")
async def status():
    return {"running": True, "version": "1.0", "host": HOST, "timestamp": datetime.datetime.now(datetime.timezone.utc)}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/screensaver/activate", summary="Activate the screensaver.")
async def screensaver_activate():
    return execute("xscreensaver-command -activate")


@app.get("/screensaver/activate", summary="Deactivate the screensaver.")
async def screensaver_deactivate():
    return execute("xscreensaver-command -deactivate")
