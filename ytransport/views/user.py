import aiohttp_jinja2
from aiohttp_session import get_session


@aiohttp_jinja2.template("login.html")
async def login(request):
    session = await get_session(request)
    session["a"] = 3
    return {}


@aiohttp_jinja2.template("login.html")
async def login_post(request):
    return {}
