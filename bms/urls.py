from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginUser, name='loginUser'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('ticketStatus', views.ticketStatus, name='ticketStatus'),
    path('issueTicket/<str:id>', views.issueTicket, name='issueTicket'),
    path('cancelTicket/<str:id>', views.cancelTicket, name='cancelTicket'),
    path('buslist', views.busList, name='busList'),
    path('addBus', views.addBus, name='addBus'),
    path('createBus', views.createBus, name='createBus'),
    path('editBus/<str:id>', views.editBus, name='editBus'),
    path('disableBus/<str:id>', views.disableBus, name='disableBus'),
    path('enableBus/<str:id>', views.enableBus, name='enableBus'),

    # path('passenger/confirm/<str:id>', views.confirmPassenger, name='confirmPassenger')

]
