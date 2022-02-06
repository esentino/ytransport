from typing import Coroutine

import pytest

from ytransport.action import (
    NotEnoughCashForBuyTruck,
    UserExistsError,
    WeakPasswordError,
    buy_truck,
    generate_password,
    login,
    register,
    verify_password,
)
from ytransport.models import STARTING_MONEY, Player, Town, Truck


@pytest.mark.asyncio
async def test_buy_truck_enough_money_should_return_player_truck(center_town: Coroutine[None, None, Town]):
    town = await center_town
    truck = await Truck.create(name="abc", price=100, speed=3, max_load=1000)
    player = await Player.create(username="cba", password="motyka123", money=300, town=town)
    player_truck = await buy_truck(truck, player)
    await player.refresh_from_db()
    assert player.money == 200
    assert player_truck.player == player
    assert player_truck.truck == truck


@pytest.mark.asyncio
async def test_buy_truck_not_enough_money_should_raise_error(center_town: Coroutine[None, None, Town]):
    town = await center_town
    truck = await Truck.create(name="abc", price=100, speed=3, max_load=1000)
    player = await Player.create(username="cba", password="motyka123", money=0, town=town)
    with pytest.raises(NotEnoughCashForBuyTruck):
        await buy_truck(truck, player)
    await player.refresh_from_db()
    assert player.money == 0
    assert await player.trucks.all().count() == 0


@pytest.mark.asyncio
async def test_register_with_existing_username_should_raise_user_exists_error(center_town: Coroutine[None, None, Town]):
    town = await center_town
    username = "wojtek"
    await Player.create(username=username, password="whocare", town=town)
    with pytest.raises(UserExistsError):
        await register(username, "anypassword", town)


@pytest.mark.parametrize("password", ("1Szort", "missing_big_letter", "MISSING_SMALL_LETTER"))
@pytest.mark.asyncio
async def test_register_password_not_meet_criteria_raise(center_town: Coroutine[None, None, Town], password: str):
    town = await center_town
    username = "wojtek"
    with pytest.raises(WeakPasswordError):
        await register(username, password, town)


@pytest.mark.asyncio
async def test_register_success(center_town: Coroutine[None, None, Town]):
    town = await center_town
    username = "tomek"
    password = "Tomek1234"
    player = await register(username, password, town)
    assert player.money == STARTING_MONEY
    assert player.username == username
    assert player.town == town
    assert await verify_password(player.password, password)


@pytest.mark.asyncio
async def test_login_with_valid_password(center_town: Coroutine[None, None, Town]):
    town = await center_town
    password = "DyWaN123"
    hashed_password = await generate_password(password)
    username = "seba"
    player = await Player.create(username=username, password=hashed_password, town=town)

    player_to_log_in = await login(username, password)

    assert player == player_to_log_in


@pytest.mark.asyncio
async def test_login_with_invalid_password_should_return_none(center_town: Coroutine[None, None, Town]):
    town = await center_town
    password = "DyWaN123"
    hashed_password = await generate_password(password)
    username = "seba"
    await Player.create(username=username, password=hashed_password, town=town)

    player_to_log_in = await login(username, "very_but_password")

    assert player_to_log_in is None
