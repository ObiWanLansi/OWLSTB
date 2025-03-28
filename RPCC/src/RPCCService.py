import os
import uvicorn
import datetime
import socket
import fastapi
import tomllib
import jinja2

from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


HOST = socket.gethostname()
VERSION = "1.0"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def loadConfig() -> dict:
    with open("config.toml", "rb") as f:
        return tomllib.load(f)


def loadCommands() -> dict:
    with open("commands.toml", "rb") as f:
        return tomllib.load(f)


config = loadConfig()
topics_and_commands = loadCommands()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def systemExecute(command: str) -> dict:

    # print(f"Execute '{command}'")

    buffer = ""

    p = os.popen(command)

    for row in p:
        buffer += row

    exitcode = p.close()

    return {
        "exitcode": exitcode,
        "message": buffer
    }


def execute(topic: str, command: str) -> dict:
    if topic not in topics_and_commands:
        return {
            "exitcode": "-42",
            "message": f"Topic '{topic}' not found!"
        }

    if command not in topics_and_commands[topic]:
        return {
            "exitcode": "-42",
            "message": f"Command '{command}' not found!"
        }

    return systemExecute(topics_and_commands[topic][command]["command"])

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app = fastapi.FastAPI()
app.title = "Raspberry Pi Command & Control"
app.description = "Remote functions for a raspberry pi which can be called with url's."
app.version = VERSION
app.contact = {
    "name": "ObiWanLansi",
    "url": "https://github.com/ObiWanLansi/OWLSTB/tree/main/RPCC"
}
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/static/404.html")


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./favicon.ico")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/status", summary="Return the current status of the server.")
async def status():
    return {"running": True, "version": VERSION, "host": HOST, "timestamp": datetime.datetime.now(datetime.timezone.utc)}


@app.get("/commands", summary="Provides all topics with their commands.")
async def commands():
    return topics_and_commands


@app.get("/command/{topic}/{command}", summary="Execute the comman from the given topic.")
async def command(topic: str, command: str):
    return execute(topic, command)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/gui", response_class=HTMLResponse)
async def gui():
    with open(r".\templates\gui.html", "rt") as f:
        template = jinja2.Template(f.read())
    return template.render(topics_and_commands=topics_and_commands)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":

    # webbrowser.open_new_tab("http://127.0.0.1:1510/docs")
    # webbrowser.open_new_tab("http://127.0.0.1:1510/status")

    uvicorn.run("RPCCService:app", host=config["server"]["host"], port=config["server"]["port"], log_level="info", reload=True)

    # result = execute("test", "test")
    # result = systemExecute("ipconfig")
    # result = systemExecute(r"O:\OWLSTB\RPCC\dummyapp\bin\Release\net9.0\dummyapp.exe")
