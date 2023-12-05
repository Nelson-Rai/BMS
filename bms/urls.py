from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginUser, name='loginUser'),
    path('register', views.register, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('ticketStatus', views.ticketStatus, name='ticketStatus'),
    path('printTicket/<str:id>', views.printTicket, name='printTicket'),
    path('cancelTicket/<str:id>', views.cancelTicket, name='cancelTicket'),
    path('buslist', views.busList, name='busList'),

    # path('passenger/confirm/<str:id>', views.confirmPassenger, name='confirmPassenger')

]
