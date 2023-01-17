from tortoise import Tortoise

from app.settings import APP_MODELS


async def connect(db_url: str, generate_schemas: bool = True, create_db: bool = False):
    await Tortoise.init(
        db_url=db_url,
        modules={'models': APP_MODELS},
        _create_db=create_db
    )
    if generate_schemas:
        await Tortoise.generate_schemas()


async def close():
    return await Tortoise.close_connections()


async def drop():
    return await Tortoise._drop_databases()
