import random
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.db.models import Count

from rent.forms import CityForm
from rent.models import Owner_Ship, City, Rent_Date, Reservation

from tp_metodologia3.settings import ROOT_DIR

# Create your views here.
def welcome(request, city_id=''):
    orderType = ''
    if city_id:
        city = City.objects.get(id=city_id)
    else:
        city = False

    if request.GET:
        orderType = request.GET['orderby']

    propiedades = orderForType(orderType)
    ciudades = City.objects.all()
    propiedadesXciudad = Owner_Ship.objects.values('city').annotate(city_count=Count('city')).order_by(
        '-city_count')

    return render(request, "rent/welcome.html", {'propiedades_list': propiedades,
                                                            'ciudades_list': ciudades, 'root': ROOT_DIR,
                                                            'propiedades_por_ciudad': propiedadesXciudad,
                                                            'city': city})

def orderForType(orderType):
    if orderType:
        if orderType == 'higher_price':
            return Owner_Ship.objects.all().order_by('-price')
        elif orderType == 'lower_price':
            return Owner_Ship.objects.all().order_by('price')
        elif orderType == 'higher_capacity':
            return Owner_Ship.objects.all().order_by('-capacity')
        else:
            return Owner_Ship.objects.all().order_by('capacity')
    else:
        return Owner_Ship.objects.all()

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "application/register.html", {'form': form})


def detail(request, owner_ship_id):
    o = Owner_Ship.objects.get(id=owner_ship_id)
    dates = Date_Rent.objects.filter(owner_ship=o).filter(reservation=None)
    ciudades = City.objects.all()
    totalcapacity = o.capacity + 1
    capacity = range(1, totalcapacity)
    msg = ''

    if request.method == 'POST':
        date_list = request.POST.getlist('dates')
        reservation = Reservation(date=datetime.now(), code=random.randrange(999, 99999), total=int(o.price*len(date_list)), owner_ship=o)
        reservation.save()
        for date in date_list:
           date_new = Date_Rent.objects.filter(date=date).first()
           date_new.reservation = reservation
           date_new.save()

    return render(request, "application/detail.html",
                      {'ciudades_list': ciudades, 'owner_ship': o, 'capacity': capacity, 'dates': dates})


def reservation(request):
    return render(request, "application/reservationdetail.html")


def ownershipform(request):
    # Si estamos identificados devolvemos la portada
    ciudadesList = City.objects.all()
    error = ''
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['desc']
        capacity = request.POST['capacity']
        price = request.POST['price']
        city = request.POST['city']
        my_city = ciudadesList.filter(name=city).first()
        image = request.FILES.get('file')
        if name is not None:
            p = Owner_Ship(name=name, description=description, price=price, capacity=capacity, city=my_city,
                           owner=request.user, image=image)
            p.save()
        else:
            error = 'Ups, algo ha ocurrido'
    return render(request, "application/ownershipform.html",
                      {'ciudades_list': ciudadesList, 'error': error, 'msg': msg})

def cityform(request):
    # Si estamos identificados devolvemos la portada
    error = ''
    msg = ''
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.save()
            msg = 'Cargado Correctamente'
        else:
            error = 'La ciudad debe tener nombre'
    return render(request, "application/cityform.html", {'error': error, 'msg': msg, 'form': form})
    msg = ''

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                print('entro')
                return redirect('/')

    return render(request, "rent/login.html", {'form': form})


def logout(request):
    do_logout(request)
    return redirect('/')
