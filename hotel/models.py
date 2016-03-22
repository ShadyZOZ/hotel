from django.db import models

class AdminUsersInfo(models.Model):
    username = models.CharField('username', max_length=20)
    password = models.CharField('password', max_length=20)
    privilege = models.CharField('privilege', max_length=10)

    def __str__(self):
        return self.username

class OrderInfo(models.Model):
    roomId = models.CharField('roomId', max_length=4)
    clientId = models.CharField('clientId', max_length=8)
    checkInDate = models.CharField('checkInDate', max_length=10)
    checkOutDate = models.CharField('checkOutDate', max_length=10)
    payed = models.BooleanField('payed', default=False)

    def __str__(self):
        return str(self.id)

class ReservationInfo(models.Model):
    roomId = models.CharField('roomId', max_length=4)
    clientName = models.CharField('clientName', max_length=20)
    clientPhone = models.CharField('clientPhone', max_length=11)
    checkInDate = models.CharField('checkInDate', max_length=10)
    checkOutDate = models.CharField('checkOutDate', max_length=10)

    def __str__(self):
        return str(self.id) + ' ' + self.roomId + ' ' + self.clientName

class ClientInfo(models.Model):
    clientName = models.CharField('clientName', max_length=20)
    clientIdNumber = models.CharField('clientIdNumber', max_length=18)
    clientPhone = models.CharField('clientPhone', max_length=11)

    def __str__(self):
        return self.clientName

class RoomInfo(models.Model):
    ROOMCONDITION_CHOICE = (
        ('available', 'available'),
        ('reserved', 'reserved'),
        ('sold', 'sold'),
    )
    roomId = models.CharField('roomId', max_length=4)
    roomPrice = models.CharField('roomPrice', max_length=4)
    roomType = models.CharField('roomType', max_length=5)
    roomCondition = models.CharField('roomCondition', choices=ROOMCONDITION_CHOICE, max_length=9)

    def __str__(self):
        return self.roomId + ' ' + self.roomType
