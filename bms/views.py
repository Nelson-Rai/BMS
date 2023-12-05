from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, busRoute, Passenger, bookTicket
from django.db.models import Q

# Create your views here.


@login_required(login_url='loginUser')
def index(request):
    busRoutes = busRoute.objects.all()
    
    context={'busRoutes':busRoutes}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        destination_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        vehicles_list = Vehicle.objects.filter(source=source_r, destination=destination_r, date=date_r)
        # vehicles = Vehicle.objects.filter(source=source_r, destination=destination_r, date=date_r)
        # context = {'vehicles':vehicles}
        request.session['date'] = date_r
        request.session.save()

        if vehicles_list:
            # context={'vehicles_list':vehicles_list}
            return render(request, 'bms/index.html', locals())
        else:
            context["error"] = "No bus available."
            return render(request, 'bms/index.html', context)
    return render(request, 'bms/index.html', context)
    # availables = Vehicle.objects.get('total_seats')
    # available = Vehicle.objects.get('available_seats')


@login_required(login_url='loginUser')
def busList(request):
    vehicles = Vehicle.objects.all()

    context = {'vehicles':vehicles}
    return render(request, 'bms/busList.html', context)



@login_required(login_url='loginUser')
def printTicket(request, id):
    vehicle = Vehicle.objects.get(id=id)
    ticketNum = bookTicket.objects.latest('ticketNumber')
    # here when ticketNum is null it generates error. solve it.
    user = request.user
    # booked_seats = int(request.POST.get('booked_seats'))
    if request.method == "POST":
        book_ticket = int(request.POST.get('book_ticket'))
        book = vehicle.booked_seats
        date = request.session.get('date')
        # if ticketNum is None:
        #     ticket=1
        ticket = ticketNum.ticketNumber + 1
        cost = vehicle.price*book_ticket
        book_seats = book+book_ticket
        available = vehicle.available_seats-book_ticket
        Vehicle.objects.filter(id=id).update(booked_seats=book_seats, available_seats=available)
        bookTicket.objects.create(user=user,vehicle_id=vehicle, date=date, booked_ticket=book_ticket,ticketNumber=ticket, cost=cost)

        context = {
            'vehicle':vehicle, 
            'book_ticket':book_ticket, 
            'ticketNumber':ticket,
            'cost':cost
            }
        return render(request, 'bms/printTicket.html', context)
    return HttpResponse("Please select number of tickets")

@login_required(login_url='loginUser')
def ticketStatus(request):
    user = request.user
    if request.user: 
        tickets = bookTicket.objects.filter(user=user)

    context ={ 'tickets':tickets, 'user':user }
    return render(request, 'bms/ticketStatus.html',context)

@login_required(login_url='loginUser')
def cancelTicket(request, id):
    bookTicket.objects.filter(id=id).update(ticket_status=False)
    return redirect('ticketStatus')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not match.")

    context = {}
    return render(request, 'bms/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginUser')


def register(request):
    if request.POST:
        username = request.POST.get('username')
        email_address = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password :
            User.objects.create_user(username=username, email=email_address, password = password)
            return redirect('loginUser')
        else:
            return render(request, 'bms/register.html', {'error': 'Passwords do not matched.'})
    context = {}
    return render(request, 'bms/register.html', context)

