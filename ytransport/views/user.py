import aiohttp_jinja2
from aiohttp.web import View
from aiohttp.web_request import Request
from aiohttp_session import get_session


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
    def get(self):
        return {}

    @aiohttp_jinja2.template("register.html")
    def post(self):
        return {}
