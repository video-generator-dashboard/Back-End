from .db.database import init_db
from fastapi import FastAPI
from .api.v1 import routes
from .core.config import config_run

app = FastAPI()
config_run(app)

app.include_router(routes.api_router)

@app.on_event("startup")
def startup_event():
    init_db()


