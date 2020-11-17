from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def registerUser(request):
    errorsFromValidator = User.objects.registerValidator(request.POST)
    if len(errorsFromValidator.items()) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.create(first_name=request.POST['form_fname_register'], last_name=request.POST['form_lname_register'], email=request.POST['form_email_register'], password=request.POST['form_pw1_register'])
    request.session['loggedInUser'] = user.id
    return redirect('/travels')

def travelsPage(request):
    if 'loggedInUser' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    user = User.objects.get(id=request.session['loggedInUser'])
    context = {
        'thisUser' : User.objects.get(id=request.session['loggedInUser']),
        'allTrips' : Trip.objects.all(),
        'userTrips' : Trip.objects.filter(travellers=user.id),
        'nonUserTrips' : Trip.objects.exclude(travellers=user.id)
    }
    return render(request, 'travelsPage.html', context)

def addTripPage(request):
    if 'loggedInUser' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    return render(request, 'addTripPage.html')

def registerTrip(request):
    errorsFromValidator = Trip.objects.tripValidator(request.POST)
    if len(errorsFromValidator.items()) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/addTrip')
    user = User.objects.get(id=request.session['loggedInUser'])
    Trip.objects.create(destination=request.POST['trip_destination_register'],creator=user.first_name, start_date=request.POST['trip_start_register'], end_date=request.POST['trip_end_register'], description=request.POST['trip_description_register'])
    thisTrip = Trip.objects.last()
    thisTrip.travellers.add(user)
    return redirect('/travels')

def login(request):
    errorsFromValidator = User.objects.loginValidator(request.POST)
    if len(errorsFromValidator.items()) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.get(email=request.POST['form_email_login'])
    request.session['loggedInUser'] = user.id
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def showTripPage(request, tripID):
    if 'loggedInUser' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    selectedTrip = Trip.objects.get(id=tripID)
    context = {
        'thisTrip' : Trip.objects.get(id=tripID),
        'allJoiners' : selectedTrip.travellers.all()
    }
    return render(request, 'showTrip.html', context)

def joinTrip(request, tripID):
    user = User.objects.get(id=request.session['loggedInUser'])
    trip = Trip.objects.get(id=tripID)
    trip.travellers.add(user)
    return redirect('/travels')

def removeSelfFromTrip(request, tripID):
    user = User.objects.get(id=request.session['loggedInUser'])
    trip = Trip.objects.get(id=tripID)
    trip.travellers.remove(user)
    return redirect('/travels')

def deleteTrip(request, tripID):
    trip = Trip.objects.get(id=tripID)
    trip.delete()
    return redirect('/travels')
