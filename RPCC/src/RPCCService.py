import datetime
import socket
import fastapi
import tomllib

from rich import print

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


HOST = socket.gethostname()
VERSION = "1.0"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def loadConfig() -> dict:
    with open("commands.toml", "rb") as f:
        return tomllib.load(f)


def execute(command: str) -> dict:
    print(f"Execute '{command}'")
    return {
        "exitcode": "-42",
        "stdout": None
    }

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


topics_and_commands = loadConfig()

app = fastapi.FastAPI()
app.title = "Raspberry Pi Command & Control"
app.description = "Remote functions for a raspberry pi which can be called with url's."
app.version = VERSION
app.contact = {
    "name": "ObiWanLansi",
    "url": "https://github.com/ObiWanLansi/OWLSTB/tree/main/RPCC"
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/status", summary="Return the current status of the server.")
async def status():
    return {"running": True, "version": VERSION, "host": HOST, "timestamp": datetime.datetime.now(datetime.timezone.utc)}


@app.get("/commands")
async def commands():
    return topics_and_commands


@app.get("/command/{topic}/{command}")
async def command(topic: str, command: str):
    return {"topic": topic, "command": command}


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# @app.get("/screensaver/activate", summary="Activate the screensaver.")
# async def screensaver_activate():
#     return execute("xscreensaver-command -activate")


# @app.get("/screensaver/deactivate", summary="Deactivate the screensaver.")
# async def screensaver_deactivate():
#     return execute("xscreensaver-command -deactivate")
