import aiohttp_jinja2


@aiohttp_jinja2.template("login.html")
async def login(request):
    return {}
