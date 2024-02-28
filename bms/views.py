from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, busRoute, bookTicket
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from datetime import datetime, timedelta



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
            time_differences = []
            # instance1 = Vehicle.objects.get('departure')
            # instance2 = Vehicle.objects.get('arrive')
            if len(vehicles_list) > 1:
                for i in range(len(vehicles_list)-1):
                    start_time = datetime.strptime(str(vehicles_list[i].departure), '%H:%M:%S').time()
                    end_time = datetime.strptime(str(vehicles_list[i].arrive), '%H:%M:%S').time()

                    # Calculate the time difference
                    time_difference = timedelta(
                        hours=end_time.hour - start_time.hour, 
                        minutes=end_time.minute - start_time.minute,
                        seconds=end_time.second - start_time.second
                        )

                    # Display the time difference
                    hours, remainder = divmod(time_difference.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_difference_formatted = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
                    time_differences.append(time_difference_formatted)

            else :
                for i in range(len(vehicles_list)):
                    start_time = datetime.strptime(str(vehicles_list[i].departure), '%H:%M:%S').time()
                    end_time = datetime.strptime(str(vehicles_list[i].arrive), '%H:%M:%S').time()

                    # Calculate the time difference
                    time_difference = timedelta(
                        hours=end_time.hour - start_time.hour, 
                        minutes=end_time.minute - start_time.minute,
                        seconds=end_time.second - start_time.second
                        )

                    # Display the time difference
                    hours, remainder = divmod(time_difference.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_difference_formatted = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
                    time_differences.append(time_difference_formatted)
            

            context = {'time_differences': time_differences}
            # context={'vehicles_list':vehicles_list}
            return render(request, 'bms/index.html', locals())
        else:
            context["error"] = "No bus available."
            return render(request, 'bms/index.html', context)
    return render(request, 'bms/index.html', context)

@login_required(login_url='loginUser')
def busRoutes(request):
    routes = busRoute.objects.all()
    successMessages = messages.get_messages(request)
    context = {'routes':routes, 'messages':successMessages}
    return render(request, 'bms/busRoutes.html', context)

@login_required(login_url='loginUser')
def addRoute(request):
    if request.method == 'POST' and request.user.is_superuser:
        name = request.POST.get('routeName')

        if busRoute.objects.filter(name=name).exists():
            messages.error(request, "Bus route with this Name already exists..") 
            return HttpResponseRedirect(request.path_info)
            
        busRoute.objects.create(name=name) 
        messages.success(request, 'New Route added Successfully')
        return redirect('busRoutes')
    elif not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    else:
        return render(request, 'bms/addRoute.html')

@login_required(login_url='loginUser')
def editRoute(request, id):
    route = busRoute.objects.get(id=id)
    if request.user.is_superuser:
        if request.method == 'POST' :
            name = request.POST.get('routeName')
            if busRoute.objects.filter(name=name).exists():
                messages.error(request, "Bus route with this Name already exists..") 
                return HttpResponseRedirect(request.path_info)
            busRoute.objects.filter(id=id).update(name=name) 
            messages.success(request, 'Route edited Successfully')
            return HttpResponseRedirect(request.path_info)
        context = {
                'route':route,
                }
        return render(request, 'bms/editRoute.html', context)
    else:
        return HttpResponseForbidden("You do not have permission to access this page.") 

@login_required(login_url='loginUser')
def deleteRoute(request, id):
    route = get_object_or_404(busRoute, id=id)
    route.delete()
    messages.success(request, 'Route Deleted Successfully')
    return redirect(busRoutes)


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
    if  request.user.is_superuser:
        return render(request, 'bms/addBus.html', context)
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")

@login_required(login_url='loginUser')
def createBus(request):
    if request.method == 'POST' and request.user.is_superuser:
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
        if Vehicle.objects.filter(name=name).exists():
            messages.error(request, "Bus with this Name already exists..") 
            return redirect('addBus')
        elif Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            messages.error(request, "Bus with this vehicle number already exists..") 
            return redirect('addBus')
        Vehicle.objects.create(name=name, vehicle_number=vehicle_number, source=source, destination=destination, date=date, departure=departure, arrive=arrive, available_seats=available_seats, price=price) 

        messages.success(request, 'New Bus added Successfully')
        return redirect('busList')
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")
    

@login_required(login_url='loginUser')
def editBus(request, id):
    # vehicle = Vehicle.objects.get(id=id)
    busRoutes = busRoute.objects.all()
    vehicle = Vehicle.objects.get(id=id)

    if request.user.is_superuser:
        if request.method == 'POST' :
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
    else:
       return HttpResponseForbidden("You do not have permission to access this page.") 

@login_required(login_url='loginUser')
def disableBus(request, id):
    if  request.user.is_superuser:
        Vehicle.objects.filter(id=id).update(v_status=False)
        return redirect('busList')
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")



@login_required(login_url='loginUser')
def enableBus(request, id):
    if  request.user.is_superuser:
        Vehicle.objects.filter(id=id).update(v_status=True)
        return redirect('busList')
    else:
        return HttpResponseForbidden("You do not have permission to access this page.")

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
def print(request):
    return render(request, 'printTicket.html')


@login_required(login_url='loginUser')
def ticketStatus(request):

    user = request.user
    if request.user: 
        tickets = bookTicket.objects.filter(user=user)

    context ={ 
                'tickets':tickets,
                'user':user,
                # 'vehicle': vehicle,
                 }
    return render(request, 'bms/ticketStatus.html',context)

@login_required(login_url='loginUser')
def searchTicket(request):
    user = request.user
    ticket = int(request.GET.get('search'))
    if ticket:
        if user:
            tickets = bookTicket.objects.filter(user=user, ticketNumber=ticket)
            if not tickets:
                messages.error(request, '!!! Ticket Not Found !!!')           
        else:
            tickets = bookTicket.objects.none()

    context = {
                'tickets':tickets,
                'user':user,
            }
    return render(request, 'bms/ticketStatus.html',context)

@login_required(login_url='loginUser')
def cancelTicket(request, id):
    user = request.user
    if user: 
        ticket = bookTicket.objects.get(id=id, user=user)
        vehicle = ticket.vehicle_id
        seats = vehicle.available_seats
        cancel = ticket.booked_ticket
        vehicle.available_seats = seats + cancel
        vehicle.save()
        ticket.ticket_status=False
        ticket.save()
        return redirect('ticketStatus')
    return HttpResponse("You are not authorized.")

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

