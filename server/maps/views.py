from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from maps.models import Marker
from server.forms import SignUpForm, LoginForm, LocationForm


@login_required(login_url='/login')
def home_view(request):
    queryset_json = serializers.serialize('json', Marker.objects.filter(user=request.user))

    return render(request, "home.html", {
        "mp_token": settings.MAPBOX_TOKEN,
        "markers": queryset_json
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')
            return render(request, 'login.html', {'errors': {"failed": "Can not authenticate"}})
        else:
            return render(request, 'login.html', {'errors': form.errors})

    return render(request, 'login.html', {'errors': []})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('home')
        else:
            return render(request, 'register.html', {'errors': form.errors})

    return render(request, 'register.html', {'errors': []})


def log_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')


@login_required(login_url='/login')
def change_location(request):
    form = LocationForm(request.POST)
    if form.is_valid():
        location, created = Marker.objects.get_or_create(
            user=request.user,
            action_type=form.cleaned_data.get('activity')
        )
        location.lng = form.cleaned_data.get('lng')
        location.lat = form.cleaned_data.get('lat')

        location.save()
        return HttpResponse({"done": True}, status=200)
    else:
        return HttpResponse({"err": form.errors}, status=417)