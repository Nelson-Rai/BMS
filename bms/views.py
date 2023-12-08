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
        request.session['date'] = date_r
        request.session.save()

        if vehicles_list:
            # context={'vehicles_list':vehicles_list}
            return render(request, 'bms/index.html', locals())
        else:
            context["error"] = "No bus available."
            return render(request, 'bms/index.html', context)
    return render(request, 'bms/index.html', context)


@login_required(login_url='loginUser')
def busList(request):
    vehicles = Vehicle.objects.all()
    successMessages = messages.get_messages(request)
    context = {'vehicles':vehicles, 'messages':successMessages}
    return render(request, 'bms/busList.html', context)

@login_required(login_url='loginUser')
def addBus(request):
    busRoutes = busRoute.objects.all()
    context = {'busRoutes':busRoutes}
    return render(request, 'bms/addBus.html', context)


@login_required(login_url='loginUser')
def createBus(request):
    if request.method == 'POST':
        name = request.POST.get('Vname')
        vehicle_number = request.POST.get('Vnumber')
        sourceid = int(request.POST.get('source'))
        source = busRoute.objects.get(id=sourceid)
        destinationid = int(request.POST.get('destination'))
        destination = busRoute.objects.get(id=destinationid)
        date = request.POST.get('date')
        departure = request.POST.get('Dtime')
        arrive = request.POST.get('Atime')
        available_seats = request.POST.get('seats')
        price = request.POST.get('price')
        Vehicle.objects.create(name=name, vehicle_number=vehicle_number, source=source, destination=destination, date=date, departure=departure, arrive=arrive, available_seats=available_seats, price=price) 

        messages.success(request, 'New Bus added Successfully')
        return redirect('busList')
    return HttpResponse('Something Went Wrong') 

@login_required(login_url='loginUser')
def editBus(request, id):
    # vehicle = Vehicle.objects.get(id=id)
    busRoutes = busRoute.objects.all()
    vehicle = Vehicle.objects.get(id=id)

    
    if request.method == 'POST':
        name = request.POST.get('Vname')
        vehicle_number = request.POST.get('Vnumber')
        sourceid = int(request.POST.get('source'))
        source = busRoute.objects.get(id=sourceid)
        destinationid = int(request.POST.get('destination'))
        destination = busRoute.objects.get(id=destinationid)
        date = request.POST.get('date')
        departure = request.POST.get('Dtime')
        arrive = request.POST.get('Atime')
        available_seats = request.POST.get('seats')
        price = request.POST.get('price')
        Vehicle.objects.filter(id=id).update(name=name, vehicle_number=vehicle_number, source=source, destination=destination, date=date, departure=departure, arrive=arrive, available_seats=available_seats, price=price) 

        messages.success(request, 'Bus edited Successfully')
        return redirect('busList')
    context = {
        'busRoutes':busRoutes,
        'vehicle' : vehicle,
        }
    return render(request, 'bms/editBus.html', context)

@login_required(login_url='loginUser')
def disableBus(request, id):
    Vehicle.objects.filter(id=id).update(v_status=False)
    return redirect('busList')

@login_required(login_url='loginUser')
def enableBus(request, id):
    Vehicle.objects.filter(id=id).update(v_status=True)
    return redirect('busList')

@login_required(login_url='loginUser')
def issueTicket(request, id):
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

