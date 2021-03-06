import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent

TORTOISE_ORM = {
    "connections": {
        # Dict format for connection
        # Using a DB_URL string
        "default": "postgres://postgres:coderslab@localhost:5432/ytransport"
    },
    "apps": {
        "ytransport": {
            "models": ["ytransport.models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            "default_connection": "default",
        }
    },
}
SESSION_SECRET_KEY = b"xa7aeN3fohcheeka5aiceez7eeGee7ae"

DEBUG = True
MINIMUM_PASSWORD_LENGTH = 8
