import os
import logging

from fastapi import FastAPI

logging.basicConfig(
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    level=os.environ.get("LOGGING", "INFO"),
)

app = FastAPI()


@app.get("/api/v1/device_information")
async def get_device_information():
    return {"status": "Ok"}
