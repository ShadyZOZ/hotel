from django.contrib import admin

from .models import AdminUsersInfo, OrderInfo, ReservationInfo, ClientInfo, RoomInfo

class RoomInfoAdmin(admin.ModelAdmin):
    list_display = ['roomId', 'roomType', 'roomPrice', 'roomCondition']
    list_filter = ['roomType', 'roomCondition']
    search_field = ['roomId']

class ClientInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'clientName', 'clientIdNumber', 'clientPhone']
    search_field = ['id', 'clientName', 'clientIdNumber', 'clientPhone']

class ReservationInfoAdmin(admin.ModelAdmin):
    list_display = ['roomId', 'clientName', 'clientPhone', 'checkInDate', 'checkOutDate']
    list_filter = ['roomId', 'clientName', 'clientPhone', 'checkInDate', 'checkOutDate']
    search_field = ['roomId', 'clientName', 'clientPhone']

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['roomId', 'clientId', 'checkInDate', 'checkOutDate', 'payed']
    list_filter = ['roomId', 'clientId', 'checkInDate', 'checkOutDate', 'payed']
    search_field = ['roomId', 'clientId']

admin.site.register(RoomInfo, RoomInfoAdmin)
admin.site.register(ClientInfo, ClientInfoAdmin)
admin.site.register(ReservationInfo, ReservationInfoAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
