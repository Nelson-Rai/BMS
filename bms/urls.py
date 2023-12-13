from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginUser, name='loginUser'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('ticketStatus', views.ticketStatus, name='ticketStatus'),
    path('issueTicket/<str:id>', views.issueTicket, name='issueTicket'),
    path('print', views.print, name='print'),
    path('cancelTicket/<str:id>', views.cancelTicket, name='cancelTicket'),
    path('buslist', views.busList, name='busList'),
    path('addBus', views.addBus, name='addBus'),
    path('createBus', views.createBus, name='createBus'),
    path('editBus/<str:id>', views.editBus, name='editBus'),
    path('disableBus/<str:id>', views.disableBus, name='disableBus'),
    path('enableBus/<str:id>', views.enableBus, name='enableBus'),
    path('busRoutes', views.busRoutes, name='busRoutes'),
    path('addRoute', views.addRoute, name='addRoute'),
    path('editRoute/<str:id>', views.editRoute, name='editRoute'),
    path('deleteRoute/<str:id>', views.deleteRoute, name='deleteRoute'),

]
