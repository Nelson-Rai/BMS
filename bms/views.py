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
    # busRoutes = busRoute.objects.all()
    
    context={}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        destination_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        vehicles_list = Vehicle.objects.filter(source=source_r, destination=destination_r, date=date_r)
        # vehicles = Vehicle.objects.filter(source=source_r, destination=destination_r, date=date_r)
        # context = {'vehicles':vehicles}
        if vehicles_list:
            # context={'vehicles_list':vehicles_list}
            return render(request, 'bms/index.html', locals())
        else:
            context["error"] = "No bus available."
            return render(request, 'bms/index.html', context)
    return render(request, 'bms/index.html')
    # availables = Vehicle.objects.get('total_seats')
    # available = Vehicle.objects.get('available_seats')


# def savePassenger(request, id):
#     vehicle = Vehicle.objects.get(id=id)
#     request.session.clear()
#     passengers = Passenger.objects.all()
#     context = {'vehicle':vehicle, 'passengers':passengers}
#     return render(request, 'bms/passenger.html', context)

# def createPassenger(request, id):
#     vehicle = Vehicle.objects.get(id=id)
#     context = {'vehicle':vehicle}
#     names =[]
#     ages = []
#     genders = []
#     if request.method == 'POST':
#         names = request.session.get('names', [])
#         ages = request.session.get('ages', [])
#         genders = request.session.get('genders', [])
#         for i in '012345':
#             name = request.POST.get('pname')
#             age = request.POST.get('age')
#             gender = request.POST.get('gender')
#         names.append(name)
#         ages.append(age)
#         genders.append(gender)
#         request.session['names'] = names
#         request.session['ages'] = ages
#         request.session['genders'] = genders 
#         return redirect('confirmPassenger', id)
#     return render(request, 'bms/createPassenger.html', context)


@login_required(login_url='loginUser')
def printTicket(request, id):
    vehicle = Vehicle.objects.get(id=id)
    ticketNum = bookTicket.objects.latest('ticketNumber')
    user = request.user
    # booked_seats = int(request.POST.get('booked_seats'))
    if request.method == "POST":
        book_ticket = int(request.POST.get('book_ticket'))
        book = vehicle.booked_seats
        ticket = ticketNum.ticketNumber + 1
        cost = vehicle.price*book_ticket
        book_seats = book+book_ticket
        Vehicle.objects.filter(id=id).update(booked_seats=book_seats)
        bookTicket.objects.create(user=user,vehicle_id=vehicle, booked_ticket=book_ticket,ticketNumber=ticket, cost=cost)

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
    return redirect('list')

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

