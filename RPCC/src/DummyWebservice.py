import uvicorn
import datetime
import math
import socket
import fastapi

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


XYLOPHONMUSIK = "Falsches Üben von Xylophonmusik quält jeden größeren Zwerg."

USER = {
    1: "Hans Zimmer",
    2: "Eric Clapton",
    3: "Milli Vanilli"
}

HOST = socket.gethostname()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app = fastapi.FastAPI()
app.description = "DummyWebservice"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


@app.get("/")
async def root():
    return {"success": True, "version": "1.0", "host":HOST, "timestamp": datetime.datetime.now(datetime.timezone.utc), "pi": math.pi, "answer": 42, "fib": [0, 1, 1, 2, 3, 5, 8, 13, 21], "user": USER, "message": XYLOPHONMUSIK}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    uvicorn.run("DummyWebservice:app", host="0.0.0.0", port=9999, log_level="debug", log_config="./logging_config.yaml")
