import datetime
import socket
import fastapi

from rich import print

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


HOST = socket.gethostname()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


async def execute(command: str) -> int:
    print(f"Execute '{command}'")
    return -1

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

