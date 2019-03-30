from fastapi import FastAPI
from aiofile import AIOFile
import ujson as json
import os

app = FastAPI()
base_url = os.environ['CONFIG_URI'].replace('file://', '')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/configs")
def list_configs():
    return {}


@app.get("/config/{filename}")
async def print_file(filename: str):
    async with AIOFile(os.path.join(base_url + filename), 'rb') as file:
        data = await file.read(4096)
        conf = json.loads(data)
        print(conf)
        return conf
