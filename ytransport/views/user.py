import aiohttp_jinja2
from aiohttp import web
from aiohttp.web import View
from aiohttp.web_request import Request
from aiohttp_session import get_session

from ..action import UserExistsError, WeakPasswordError, register
from ..models import Town


@aiohttp_jinja2.template("login.html")
async def login(request: Request):
    session = await get_session(request)
    session["a"] = 3
    return {}


@aiohttp_jinja2.template("login.html")
async def login_post(request):
    return {}


class LoginView(View):
    @aiohttp_jinja2.template("login.html")
    def get(self):
        return {}

    @aiohttp_jinja2.template("login.html")
    def post(self):
        return {}


class RegisterView(View):
    @aiohttp_jinja2.template("register.html")
    async def get(self):
        towns = await Town.all()
        return {"towns": towns}

    @aiohttp_jinja2.template("register.html")
    async def post(self):
        data = await self.request.post()
        towns = await Town.all()
        result_data = {"towns": towns}
        if (
            "username" in data
            and "password" in data
            and "passwordbis" in data
            and "town" in data
            and data["password"] == data["passwordbis"]
            and data["town"]
        ):
            try:
                start_town = await Town.get_or_none(id=data["town"])
                if start_town:
                    await register(username=data["username"], password=data["password"], town=start_town)
                    return web.HTTPFound(self.request.app.router["login"].url_for())
                else:
                    result_data["error"] = "Town doesn't exists"
            except UserExistsError:
                result_data["error"] = "Username is not available. Please use another one."
            except WeakPasswordError:
                result_data["error"] = "Password is poor quality (to short or missing small or big letter)"
        return result_data
