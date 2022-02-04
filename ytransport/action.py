from tortoise.expressions import F
from tortoise.transactions import atomic

from ytransport.models import Player, PlayerTruck, Truck, Town

MINIMUM_PASSWORD_LENGTH = 8


class NotEnoughCashForBuyTruck(Exception):
    def __init__(self, price: float, money: float):
        self._price = price
        self._money = money

    def __str__(self):
        return f"Not enough cash for buy truck ({self._price}$) missing {self._price-self._money}$."


class UserExists(Exception):
    def __init__(self, username: str):
        self._username = username

    def __str__(self):
        return f"Username {self._username} is not available"


class WeakPasswordError(Exception):
    pass


@atomic("default")
async def buy_truck(truck: Truck, player: Player) -> PlayerTruck:
    await player.refresh_from_db()

    if truck.price >= player.money:
        raise NotEnoughCashForBuyTruck(truck.price, player.money)

    player.money = F("money") - truck.price
    await player.save()

    return await PlayerTruck.create(truck=truck, player=player, load=0)


async def meet_password_criteria(password: str) ->bool:
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False

    if password.lower() == password:
        return False

    if password.upper() == password:
        return False


async def generate_password(password):
    pass


@atomic("default")
async def register(username:str, password:str, town:Town) -> Player:
    if await Player.exists(username=username):
        raise UserExists(username)

    if not await meet_password_criteria(password):
        raise WeakPasswordError()

    hashed_password = await generate_password(password)
