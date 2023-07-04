import os.path
import shutil

import yaml
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import database, filesystem
from .api import v1
from . import _shared as shared


# load config file, create it if not found
if not os.path.isfile("config.yaml"):
    shutil.copy(os.path.join("arcos_backend", "assets", "config.default.yaml"), "config.yaml")
with open("config.yaml") as f:
    shared.configuration = yaml.safe_load(f)

storage_cfg = shared.configuration['storage']
os.makedirs(storage_cfg['root'], exist_ok=True)
shared.database = database.Database(os.path.join(storage_cfg['root'], storage_cfg['database']))
shared.filesystem = filesystem.Filesystem(os.path.join(storage_cfg['root'], storage_cfg['filesystem']),
                                          os.path.join(storage_cfg['root'], storage_cfg['template']) if storage_cfg['template'] is not None else None,
                                          shared.configuration['filesystem']['userspace_size'])

app = FastAPI(title=shared.configuration['name'], version="0.0.1")

# tells cors to fuck off
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(v1.router)
