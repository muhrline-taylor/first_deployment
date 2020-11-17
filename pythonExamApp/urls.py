from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.registerUser),
    path('login', views.login),
    path('travels', views.travelsPage),
    path('addTrip', views.addTripPage),
    path('registerTrip', views.registerTrip),
    path('logout', views.logout),
    path('view/<int:tripID>', views.showTripPage),
    path('joinTrip/<int:tripID>', views.joinTrip),
    path('removeTrip/<int:tripID>', views.removeSelfFromTrip),
    path('deleteTrip/<int:tripID>', views.deleteTrip)
]