from typing import Optional

from nacl import pwhash
from nacl.exceptions import InvalidkeyError
from tortoise.expressions import F
from tortoise.transactions import atomic

from .conf import MINIMUM_PASSWORD_LENGTH
from .models import Player, PlayerTruck, Town, Truck


class NotEnoughCashForBuyTruck(Exception):
    def __init__(self, price: float, money: float):
        self._price = price
        self._money = money

    def __str__(self):
        return f"Not enough cash for buy truck ({self._price}$) missing {self._price-self._money}$."


class UserExistsError(Exception):
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


async def meet_password_criteria(password: str) -> bool:
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False

    if password.lower() == password:
        return False

    if password.upper() == password:
        return False

    return True


async def generate_password(password: str) -> str:
    return pwhash.str(password.encode()).decode()


async def verify_password(hashed: str, password: str) -> bool:
    # Verify return true on match password, raise InvalidkeyError on failed
    try:
        return pwhash.verify(hashed.encode(), password.encode())
    except InvalidkeyError:
        return False


async def login(username: str, password: str) -> Optional[Player]:
    player = await Player.filter(username=username).first()
    if player and await verify_password(player.password, password):
        return player
    return None


@atomic("default")
async def register(username: str, password: str, town: Town) -> Player:
    if await Player.exists(username=username):
        raise UserExistsError(username)

    if not await meet_password_criteria(password):
        raise WeakPasswordError()

    hashed_password = await generate_password(password)

    return await Player.create(username=username, password=hashed_password, town=town)
