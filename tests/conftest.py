import os

import pytest
from tortoise import Tortoise, current_transaction_map, generate_config
from tortoise.contrib.test import finalizer, initializer

from ytransport.models import Town


@pytest.fixture(autouse=True)
def init_dd():
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["ytransport.models"], db_url=db_url, app_label="ytransport")
    print(current_transaction_map)
    current_transaction_map["default"] = current_transaction_map["ytransport"]
    yield
    finalizer()


@pytest.fixture
async def center_town():
    return await Town.create(name="town", latitude=0.0, longitude=0.0)


@pytest.fixture
async def app_test_app(aiohttp_client):
    from ytransport.main import make_app

    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    config = generate_config(db_url=db_url, app_modules={"models": ["models"]})
    await Tortoise.init(config, _create_db=True)
    await Tortoise.generate_schemas(safe=False)
    yield await aiohttp_client(make_app())
    await Tortoise._drop_databases()
