from tortoise.expressions import F
from tortoise.transactions import atomic

from ytransport.models import Player, PlayerTruck, Truck


class NotEnoughCashForBuyTruck(Exception):
    def __init__(self, price: float, money: float):
        self._price = price
        self._money = money

    def __str__(self):
        return f"Not enough cash for buy truck ({self._price}$) missing {self._price-self._money}$."


@atomic("default")
async def buy_truck(truck: Truck, player: Player) -> PlayerTruck:
    await player.refresh_from_db()

    if truck.price >= player.money:
        raise NotEnoughCashForBuyTruck(truck.price, player.money)

    player.money = F("money") - truck.price
    await player.save()

    return await PlayerTruck.create(truck=truck, player=player, load=0)
