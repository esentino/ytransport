import pytest

from ytransport.action import buy_truck
from ytransport.models import Player, Town, Truck


@pytest.mark.asyncio
async def test_buy_truck_enough_money_should_return_player_truck():
    town = await Town.create(name="town", latitude=0.0, longitude=0.0)
    truck = await Truck.create(name="abc", price=100, speed=3, max_load=1000)
    player = await Player.create(username="cba", password="motyka123", money=300, town=town)
    player_truck = await buy_truck(truck, player)
    await player.refresh_from_db()
    assert player.money == 200
    assert player_truck.player == player
    assert player_truck.truck == truck
