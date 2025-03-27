import os
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


topics_and_commands = loadConfig()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def systemExecute(command: str) -> dict:
    
    print(f"Execute '{command}'")
    
    buffer = ""
    
    p =os.popen(command)
    for row in p:
        buffer += row
    ret = p.close()
    
    return {
        "exitcode": ret,
        "message": buffer
    }


def systemExecute2(command: str) -> dict:
    
    print(f"Execute '{command}'")
    
    buffer = ""
    
    with os.popen(command) as p:
        for row in p:
            buffer += row
    
    return {
        "exitcode": "-42",
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

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/status", summary="Return the current status of the server.")
async def status():
    return {"running": True, "version": VERSION, "host": HOST, "timestamp": datetime.datetime.now(datetime.timezone.utc)}


@app.get("/commands")
async def commands():
    return topics_and_commands


@app.get("/command/{topic}/{command}")
async def command(topic: str, command: str):
    return execute(topic, command)
    # return {"topic": topic, "command": command}


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# if __name__ == "__main__":
    # result = execute("test", "test")
    # result = systemExecute("ipconfig")
    # result = systemExecute(r"O:\OWLSTB\RPCC\dummyapp\bin\Release\net9.0\dummyapp.exe")
