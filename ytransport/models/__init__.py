from tortoise import models, fields

STARTING_MONEY = 50000


class Truck(models.Model):
    name = fields.CharField(max_length=255)
    price = fields.IntField()
    speed = fields.IntField()
    max_load = fields.IntField()


class Town(models.Model):
    name = fields.CharField(max_length=255)
    latitude = fields.FloatField()
    longitude = fields.FloatField()


class Transport(models.Model):
    begin = fields.ForeignKeyField('ytransport.Town', on_delete=fields.CASCADE, related_name="transports")
    destination = fields.ForeignKeyField('ytransport.Town', on_delete=fields.CASCADE, related_name="awaiting_transports")
    load = fields.IntField()
    delivered_load = fields.IntField()
    money = fields.IntField()


class Player(models.Model):
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    money = fields.IntField(default=STARTING_MONEY)
    town = fields.ForeignKeyField('ytransport.Town', on_delete=fields.CASCADE, related_name="players")


class PlayerTruck(models.Model):
    player = fields.ForeignKeyField('ytransport.Player', on_delete=fields.CASCADE, related_name="trucks")
    truck = fields.ForeignKeyField('ytransport.Truck', on_delete=fields.CASCADE, related_name="player_trucks")
    load = fields.IntField()
    transport = fields.ForeignKeyField('ytransport.Transport', on_delete=fields.CASCADE, null=True, related_name="trucks")
    start_transport = fields.DatetimeField(null=True)
