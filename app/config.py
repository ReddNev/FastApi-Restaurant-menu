from app.settings import APP_MODELS, DB_PATH


TORTOISE_ORM = {
    "connections": {"default": DB_PATH},
    "apps": {
        "models": {
            "models": APP_MODELS,
            "default_connection": "default",
        }
    },
}
