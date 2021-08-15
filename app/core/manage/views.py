from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.views import View

from app.exceptions import UIException

from app.models import (
    Station,
    College
)

from app.utils.request_handling import get_bag, redirect_back


def fetch_model_clean(model_class, pk):
    if not pk or pk == '0':
        return None
        
    try:
        model = model_class.objects.get(pk=pk)
        return model
    except model_class.DoesNotExist:
        return None

def make_station(name: str):
    
    station = Station()
    station.name = name
    station.save()
    
    return station

def make_college(name: str, station: Station):
        college = College()
        college.name = name
        college.station = station
        college.save()
        return college


def index(req):
    return render(req, "main/pages/manage.html", {
        "stations": Station.objects.all().prefetch_related('colleges'),
    })


# =========================== NEW COLLEGE ===========================
class Action_CreateCollege(View):
    def post(self, req):
        bag = get_bag(req)
        name = bag.get('name', None)

        if not name:
            raise UIException("Enter a valid name")

        try:
            station = Station.objects.get(pk=bag.get('station_id'))
        except Station.DoesNotExist:
            raise UIException('Station not found')

        make_college(name, station)
        messages.success(req, "College added successfully")
        return redirect_back(req)


# =========================== NEW STATION ===========================
class Action_CreateStation(View):

    def post(self, req: HttpRequest):
        bag = get_bag(req)

        name = bag.get('name', None)

        if not name:
            raise UIException("Enter a valid name")

        name = name.strip()

        if Station.objects.filter(name=name).exists():
            raise UIException(f"Station '{name}' already exists")

        make_station(name)
        messages.success(req, "Station added successfully")
        return redirect_back(req)
