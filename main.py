from fastapi import FastAPI

from app import db, settings
from app.rest import router


app = FastAPI()
app.include_router(router, prefix='/api/v1')


@app.on_event("startup")
async def startup():
    _settings = settings.get_settings()
    await db.connect(db_url=_settings.db_path, generate_schemas=False)


@app.on_event("shutdown")
async def shutdown():
    await db.close()
