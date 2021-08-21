import app.utils as utils
from app.models.core import College
from .context import CollegeContext, StationContext

from rest_framework import serializers
from rest_framework.decorators import api_view

from app.core.authentication import permissions

from app.exceptions import ApiException, ApiExceptionNotFound
from app.typehints import ApiRequest, ApiResponse
from app.models import Station

def make_station(name):
    st = Station()
    st.name = name
    st.save()
    return st

def make_college(name, station: Station):
    cl = College()
    cl.name = name
    cl.station = station
    cl.save()
    return cl

class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class CollegeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    station_id = serializers.IntegerField()

_global_station_context_gen = StationContext()
_global_clg_context_gen = CollegeContext()

# ======================================================================================
# ====================================== STATONS ======================================
# ======================================================================================

@api_view(['GET'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'read', 
    _global_station_context_gen
)
def station_list(request: ApiRequest):
    """
    Returns a list of stations
    """

    stations = StationSerializer(Station.objects.all(), many=True)    
    return ApiResponse(stations.data)


@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'create', 
    _global_station_context_gen
)
def station_create(request: ApiRequest):
    name = request.data.get('name', '').strip()

    data = {'created_id': '', 'created_name': ''}

    if not name:
        raise ApiException("Invalid name", data=data)

    if Station.objects.filter(name=name).exists():
        raise ApiException(f'Station \'{name}\' already exists', data=data)

    st = make_station(name)
    data['created_id'] = st.pk
    data['created_name'] = name

    return ApiResponse({
        'type': 'success',
        'msg': f'Station \'{name}\' created successfully',
        'payload': data
    })

@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'update', 
    _global_station_context_gen
)
def station_update(request: ApiRequest, station_id: int):
    name = request.data.get('name', '').strip()

    data = {'updated_id': None, 'updated_name': ''}

    if not name:
        raise ApiException("Invalid name", data=data)

    if Station.objects.filter(name=name).exists():
        raise ApiException(f'Station \'{name}\' already exists', data=data)

    updated_count = Station.objects.filter(pk=station_id).update(name=name)

    if updated_count == 0:
        raise ApiExceptionNotFound()

    data['updated_id'] = station_id
    data['updated_name'] = name

    return ApiResponse({
        'type': 'success',
        'msg': f'Station updated successfully',
        'payload': data
    })

# ======================================================================================
# ====================================== COLLEGES ======================================
# ======================================================================================

@api_view(['GET'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'read', 
    _global_clg_context_gen
)
def college_list(request: ApiRequest):
    """
    Returns a list of stations
    """

    colleges = CollegeSerializer(College.objects.all(), many=True)    
    return ApiResponse(colleges.data)

@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'create', 
    _global_clg_context_gen
)
def college_create(request: ApiRequest):
    name = request.data.get('name', '').strip()
    station_id = utils.to_int(request.data.get('station_id', 0))

    data = {'created_id': None, 'created_name': '', 'created_station_id': None}

    if not name:
        raise ApiException("Invalid name", data=data)

    if College.objects.filter(name=name).exists():
        raise ApiException(f'College \'{name}\' already exists', data=data)

    try:
        station = Station.objects.filter(pk=station_id).get()
    except Station.DoesNotExist:
        raise ApiException("Station not found", data=data)


    clg = make_college(name, station)
    data['created_id'] = clg.pk
    data['created_name'] = name
    data['created_station_id'] = station_id

    return ApiResponse({
        'type': 'success',
        'msg': f'College \'{name}\' created successfully',
        'payload': data
    })


@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'update', 
    _global_clg_context_gen
)
def college_update(request: ApiRequest, college_id: int):
    name = request.data.get('name', '').strip()
    station_id = utils.to_int(request.data.get('station_id', 0))

    data = {'updated_id': None, 'updated_name': '', 'updated_station_id': None}

    if not name:
        raise ApiException("Invalid name", data=data)

    if not Station.objects.filter(pk=station_id).exists():
        raise ApiException(f'Station not found', data=data)

    if College.objects.filter(name=name).exists():
        raise ApiException(f'College \'{name}\' already exists', data=data)

    updated_count = College.objects.filter(pk=college_id).update(name=name, station_id=station_id)

    if updated_count == 0:
        raise ApiExceptionNotFound()

    data['updated_id'] = college_id
    data['updated_name'] = name
    data['updated_station_id'] = station_id

    return ApiResponse({
        'type': 'success',
        'msg': f'College updated successfully',
        'payload': data
    })