import aiohttp_jinja2
import aiohttp_session
import jinja2
from aiohttp import web
from aiohttp_session.nacl_storage import NaClCookieStorage
from tortoise.contrib.aiohttp import register_tortoise

from .conf import BASE_DIR, DEBUG, SESSION_SECRET_KEY, TORTOISE_ORM
from .views import index
from .views.user import login, login_post


def make_app() -> web.Application:
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(BASE_DIR / "ytransport" / "templates")))
    register_tortoise(app, TORTOISE_ORM)
    app.router.add_get("", index)
    app.router.add_get("/login", login)
    app.router.add_post("/login", login_post)
    if DEBUG:
        for resource in app.router.resources():
            print(resource)
    aiohttp_session.setup(app, NaClCookieStorage(SESSION_SECRET_KEY))
    return app


application = make_app()
web.run_app(application)
