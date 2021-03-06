from fastapi import FastAPI
from aiofile import AIOFile
import ujson as json
from os.path import isdir, isfile
import os

MAX_CONFIG_FILE_SIZE = 409600

app = FastAPI()

base_url = os.path.abspath(os.environ['CONFIG_URI'].replace('file://', '')) + '/'

with open(os.path.join(base_url + 'config.json'), 'rb') as conf_file:
    config = ''.join([line.decode('utf-8') for line in conf_file.readlines()])
    app_conf = json.loads(config)


def readConfFuncGenerator(filepath, version):
    async def __readConfig():
        async with AIOFile(filepath, 'rb') as file:
            data = await file.read(MAX_CONFIG_FILE_SIZE)
            return {'version': version, 'config': json.loads(data)}

    return __readConfig


for service_dir_name in os.listdir(base_url):
    if isdir(os.path.join(base_url, service_dir_name)):
        service = service_dir_name
        service_dir = os.path.join(base_url + service_dir_name)

        latest = {}
        for version in os.listdir(service_dir):
            version_dir = os.path.join(service_dir, version)
            # print('version', version)
            if isdir(version_dir):
                for env_conf_name in os.listdir(version_dir):
                    env_conf_path = os.path.join(version_dir, env_conf_name)
                    if isfile(env_conf_path):
                        env_conf = os.path.splitext(env_conf_name)[0]
                        route_path = "/config/{}/{}/{}".format(service, version, env_conf)
                        app.get(route_path)(readConfFuncGenerator(env_conf_path, version))

                        if env_conf not in latest or latest[env_conf]['version'] < version:
                            latest[env_conf] = {
                                "version": version,
                                "config_path": env_conf_path
                            }

        for env_conf in latest:
            route_path = '/config/{}/latest/{}'.format(service, env_conf)
            # print('add ', route_path, latest[env_conf]['version'])
            app.get(route_path)(
                readConfFuncGenerator(latest[env_conf]['config_path'],
                                      latest[env_conf]['version']))


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
        # print(conf)
        return conf


@app.get("/config/{service_name}/{version}/{env_name}")
async def discover_service_configuration(service_name, version, env_name):
    # print('==', base_url,service_name, version, env_name)
    file_path = '{}{}/{}/{}.json'.format(base_url, service_name, version, env_name)
    route_path = '/config/{}/{}/{}'.format(service_name, version, env_name)
    # print('discover', file_path, route_path, isfile(file_path))
    if isfile(file_path):
        app.get(route_path)(readConfFuncGenerator(file_path, version))
        async with AIOFile(file_path, 'rb') as file:
            data = await file.read(MAX_CONFIG_FILE_SIZE)
            return {'version': version, 'config': json.loads(data)}
    else:
        return {"error": "config not found"}
