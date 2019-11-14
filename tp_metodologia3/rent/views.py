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
    order_type = ''
    if city_id:
        city = City.objects.get(id=city_id)
    else:
        city = False

    if request.GET:
        order_type = request.GET['orderby']

    if order_type:
        if order_type == 'higher_price':
            propiedades_list = Owner_Ship.objects.all().order_by('-price')
        elif order_type == 'lower_price':
            propiedades_list = Owner_Ship.objects.all().order_by('price')
        elif order_type == 'higher_capacity':
            propiedades_list = Owner_Ship.objects.all().order_by('-capacity')
        else:
            propiedades_list = Owner_Ship.objects.all().order_by('capacity')
    else:
        propiedades_list = Owner_Ship.objects.all()

    ciudades_list = City.objects.all()
    propiedades_por_ciudad = Owner_Ship.objects.values('city').annotate(city_count=Count('city')).order_by(
        '-city_count')
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "rent/welcome.html", {'propiedades_list': propiedades_list,
                                                            'ciudades_list': ciudades_list, 'root': ROOT_DIR,
                                                            'propiedades_por_ciudad': propiedades_por_ciudad,
                                                            'city': city})
    # En otro caso redireccionamos al login
    return redirect('/login')


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
    if request.user.is_authenticated:
        o = Owner_Ship.objects.get(id=owner_ship_id)
        dates = Date_Rent.objects.filter(owner_ship=o).filter(reservation=None)
        ciudades_list = City.objects.all()
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
                      {'ciudades_list': ciudades_list, 'owner_ship': o, 'capacity': capacity, 'dates': dates})
    # En otro caso redireccionamos al login
    return redirect('/login')


def reservation(request):
    return render(request, "application/reservationdetail.html")


def ownershipform(request):
    # Si estamos identificados devolvemos la portada
    ciudades_list = City.objects.all()
    error = ''
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['desc']
        capacity = request.POST['capacity']
        price = request.POST['price']
        city = request.POST['city']
        my_city = ciudades_list.filter(name=city).first()
        image = request.FILES.get('file')
        if name is not None:
            p = Owner_Ship(name=name, description=description, price=price, capacity=capacity, city=my_city,
                           owner=request.user, image=image)
            p.save()
        else:
            error = 'Ups, algo ha ocurrido'
    if request.user.is_authenticated:
        return render(request, "application/ownershipform.html",
                      {'ciudades_list': ciudades_list, 'error': error, 'msg': msg})
    # En otro caso redireccionamos al login
    return redirect('/login')


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
    if request.user.is_authenticated:
        return render(request, "application/cityform.html", {'error': error, 'msg': msg, 'form': form})
        msg = ''
    # En otro caso redireccionamos al login
    return redirect('/login')


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                do_login(request, user)
                print('entro')
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "rent/login.html", {'form': form})


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')
