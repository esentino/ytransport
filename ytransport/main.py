import aiohttp_jinja2
import jinja2
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from ytransport.conf import BASE_DIR, TORTOISE_ORM

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "ytransport" / "templates")))
register_tortoise(app, TORTOISE_ORM)
web.run_app(app)
