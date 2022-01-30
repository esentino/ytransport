import aiohttp_jinja2
import jinja2
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from .conf import BASE_DIR, TORTOISE_ORM
from .views import index
from .views.user import login

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "ytransport" / "templates")))
register_tortoise(app, TORTOISE_ORM)
app.router.add_get("", index)
app.router.add_get("/login", login)
web.run_app(app)
