from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils import timezone
from django.http import HttpResponse

from .models import AdminUsersInfo, OrderInfo, ReservationInfo, ClientInfo, RoomInfo
from .forms import ReservationForm, OrderForm, CheckOutForm

import time, datetime, json

def index(request):
    return redirect('hotel:overview')

def overview(request):
    infos = RoomInfo.objects.all()
    return render_to_response('hotel/dashboard.html', {'select': '0', 'infos': infos}, context_instance=RequestContext(request))

def reservation(request):
    if request.method == 'POST':
        reservationForm = ReservationForm(request.POST)
        if reservationForm.is_valid():
            roomId = reservationForm.cleaned_data['roomId']
            name = reservationForm.cleaned_data['name']
            phone = reservationForm.cleaned_data['phone']
            checkInDate = reservationForm.cleaned_data['checkInDate']
            checkOutDate = reservationForm.cleaned_data['checkOutDate']
            reservationInfo = ReservationInfo()
            reservationInfo.roomId = roomId
            reservationInfo.clientName = name
            reservationInfo.clientPhone = phone
            reservationInfo.checkInDate = checkInDate
            reservationInfo.checkOutDate = checkOutDate
            reservationInfo.save()
            res = RoomInfo.objects.get(roomId=roomId)
            res.roomCondition = 'reserved'
            res.save()
    else:
        reservationForm = ReservationForm()
    infos = RoomInfo.objects.all()
    return render_to_response('hotel/dashboard.html', {'select': '1', 'infos': infos, 'form': reservationForm}, context_instance=RequestContext(request))

def checkIn(request):
    if request.method == 'POST':
        orderForm = OrderForm(request.POST)
        if orderForm.is_valid():
            roomId = orderForm.cleaned_data['roomId']
            name = orderForm.cleaned_data['name']
            idNumber = orderForm.cleaned_data['idNumber']
            phone = orderForm.cleaned_data['phone']
            checkInDate = orderForm.cleaned_data['checkInDate']
            checkOutDate = orderForm.cleaned_data['checkOutDate']
            orderInfo = OrderInfo()
            orderInfo.roomId = roomId
            orderInfo.checkInDate = checkInDate
            orderInfo.checkOutDate = checkOutDate
            clientInfo = ClientInfo.objects.filter(clientIdNumber=idNumber)
            if clientInfo:
                if clientInfo[0].clientPhone != phone:
                    clientInfo[0].clientPhone = phone
                    clientInfo[0].save()
                orderInfo.clientId = clientInfo[0].id
            else:
                clientInfo = ClientInfo()
                clientInfo.clientName = name
                clientInfo.clientIdNumber = idNumber
                clientInfo.clientPhone = phone
                clientInfo.save()
                orderInfo.clientId = clientInfo.id
            orderInfo.save()
            res = RoomInfo.objects.get(roomId=roomId)
            if res.roomCondition == 'reserved':
                reservationInfo = ReservationInfo.objects.get(roomId=roomId)
                reservationInfo.delete()
            res.roomCondition = 'sold'
            res.save()
    else:
        orderForm = OrderForm()
    infos = RoomInfo.objects.all()
    return render_to_response('hotel/dashboard.html', {'select': '2', 'infos': infos, 'form': orderForm}, context_instance=RequestContext(request))

def checkOut(request):
    if request.method == 'POST':
        checkOutForm = CheckOutForm(request.POST)
        if checkOutForm.is_valid():
            roomId = checkOutForm.cleaned_data['roomId']
            roomInfo = RoomInfo.objects.get(roomId=roomId)
            roomInfo.roomCondition = 'available'
            roomInfo.save()
            orderInfos = OrderInfo.objects.filter(roomId=roomId)
            if orderInfos:
                orderInfos[len(orderInfos)-1].payed = True
                orderInfos[len(orderInfos)-1].save()
    else:
        checkOutForm = CheckOutForm()
    infos = RoomInfo.objects.all()
    return render_to_response('hotel/dashboard.html', {'select': '3', 'infos': infos, 'form': checkOutForm}, context_instance=RequestContext(request))

def orderManage(request):
    return render_to_response('hotel/dashboard.html', {'select': '4'}, context_instance=RequestContext(request))

def roomManage(request):
    return render_to_response('hotel/dashboard.html', {'select': '5'}, context_instance=RequestContext(request))

def customerManage(request):
    return render_to_response('hotel/dashboard.html', {'select': '6'}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('hotel/dashboard.html', {'select': '7'}, context_instance=RequestContext(request))

# def adminLogin(request):
#     if request.method == 'POST':
#         adminLoginForm = AdminLoginForm(request.POST)
#         if adminLoginForm.is_valid():
#             username = adminLoginForm.cleaned_data['username']
#             password = adminLoginForm.cleaned_data['password']
#             res = AdminUsers.objects.filter(username=username, password=password).exist()
#             if res:
#                 response = redirect('hotel:admin')
#                 response.set_cookie('username', username, 3600)
#                 response.set_cookie('password', password, 3600)
#                 return response
#             else:
#                 return redirect('hotel:overview')
#     else:
#         adminLoginForm = AdminLoginForm()
#     return render_to_response('hotel/basicForm.html', {'form': adminLoginForm, 'heading': 'Please Login', 'link': '/hotel/adminLogin/'}, context_instance=RequestContext(request))
#
# def admin(request):
#     username = request.COOKIES.get('username')
#     password = request.COOKIES.get('password')
#     res = AdminUsers.objects.filter(username=username, password=password).exist()
#     if res:
#         pass
#     else:
#         return redirect('hotel:adminLogin')

def returnPrice(request):
    if request.method == 'POST':
        roomId = request.POST.get('roomId')
        orderInfos = OrderInfo.objects.filter(roomId=roomId)
        orderInfo = orderInfos[len(orderInfos)-1]
        a = time.strptime(orderInfo.checkInDate, '%Y-%m-%d')
        b = time.strptime(orderInfo.checkOutDate, '%Y-%m-%d')
        a_datetime=datetime.datetime(*a[:3])
        b_datetime=datetime.datetime(*b[:3])
        days = (b_datetime.day-a_datetime.day)
        roomInfo = RoomInfo.objects.get(roomId=roomId)
        price = roomInfo.roomPrice
        total = price * days
        response = HttpResponse()
        response.write(json.dumps({'days': days, 'total': total}))
        return response
    else:
        return HttpResponse('error')

def returnCheckInInfo(request):
    if request.method == 'POST':
        roomId = request.POST.get('roomId')
        roomInfo = RoomInfo.objects.get(roomId=roomId)
        if roomInfo.roomCondition == 'reserved':
            reservationInfo = ReservationInfo.objects.get(roomId=roomId)
            clientName = reservationInfo.clientName
            clientPhone = reservationInfo.clientPhone
            checkInDate = reservationInfo.checkInDate
            checkOutDate = reservationInfo.checkOutDate
        else:
            clientName = ''
            clientPhone = ''
            checkInDate = ''
            checkOutDate = ''
        response = HttpResponse()
        response.write(json.dumps({'clientName': clientName, 'clientPhone': clientPhone, 'checkInDate': checkInDate, 'checkOutDate': checkOutDate}))
        return response
    else:
        return HttpResponse('error')

def returnRoomInfo(request):
    if request.method == 'POST':
        roomId = request.POST.get('roomId')
        orderInfo = OrderInfo.objects.filter(roomId=roomId).last()
        if orderInfo:
            checkInDate = orderInfo.checkInDate
            checkOutDate = orderInfo.checkOutDate
            clientInfo = ClientInfo.objects.get(id=orderInfo.clientId)
            clientName = clientInfo.clientName
            clientPhone = clientInfo.clientPhone
            clientIdNumber = clientInfo.clientIdNumber
        else:
            checkInDate = ''
            checkOutDate = ''
            clientName = ''
            clientPhone = ''
            clientIdNumber = ''
        # a = time.strptime(orderInfo.checkInDate, '%Y-%m-%d')
        # b = time.strptime(orderInfo.checkOutDate, '%Y-%m-%d')
        # a_datetime=datetime.datetime(*a[:3])
        # b_datetime=datetime.datetime(*b[:3])
        # days = (b_datetime.day-a_datetime.day)
        roomInfo = RoomInfo.objects.get(roomId=roomId)
        roomType = roomInfo.roomType
        roomPrice = roomInfo.roomPrice
        roomCondition = roomInfo.roomCondition
        if roomInfo.roomCondition == 'sold':
            orderInfo = OrderInfo.objects.filter(roomId=roomId).last()
            checkInDate = orderInfo.checkInDate
            checkOutDate = orderInfo.checkOutDate
            clientInfo = ClientInfo.objects.get(id=orderInfo.clientId)
            clientName = clientInfo.clientName
            clientPhone = clientInfo.clientPhone
            clientIdNumber = clientInfo.clientIdNumber
        elif roomInfo.roomCondition == 'reserved':
            reservationInfo = ReservationInfo.objects.get(roomId=roomId)
            clientName = reservationInfo.clientName
            clientPhone = reservationInfo.clientPhone
            checkInDate = reservationInfo.checkInDate
            checkOutDate = reservationInfo.checkOutDate
            clientIdNumber = ''
        else:
            checkInDate = ''
            checkOutDate = ''
            clientName = ''
            clientPhone = ''
            clientIdNumber = ''
        response = HttpResponse()
        response.write(json.dumps({'roomId': roomId, 'roomType': roomType, 'roomPrice': roomPrice, 'roomCondition': roomCondition, 'checkInDate': checkInDate, 'checkOutDate': checkOutDate, 'clientName': clientName, 'clientPhone': clientPhone, 'clientIdNumber': clientIdNumber}))
        return response
    else:
        return HttpResponse('error')
