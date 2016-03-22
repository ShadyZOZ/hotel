from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^checkIn/$', views.checkIn, name='checkIn'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkOut/$', views.checkOut, name='checkOut'),
    url(r'^returnPrice/$', views.returnPrice, name='returnPrice'),
    url(r'^returnCheckInInfo/$', views.returnCheckInInfo, name='returnCheckInInfo'),
    url(r'^returnRoomInfo/$', views.returnRoomInfo, name='returnRoomInfo'),
    url(r'^orderManage/$', views.orderManage, name='orderManage'),
    url(r'^roomManage/$', views.roomManage, name='roomManage'),
    url(r'^customerManage/$', views.customerManage, name='customerManage'),
    url(r'^about/$', views.about, name='about'),
    # url(r'^adminLogin/$', views.adminLogin, name='adminLogin'),
]
