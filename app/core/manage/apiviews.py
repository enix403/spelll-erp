from typing import Any, Type
from authzx.actions import Allow

from rest_framework import serializers
from rest_framework.decorators import api_view

from app.core.authentication.traits import TR
from app.core.authentication import permissions

from app.exceptions import ApiException, ApiExceptionNotFound
from app.typehints import ApiRequest, ApiResponse
from app.models import Station

def make_station(name):
    st = Station()
    st.name = name
    st.save()
    return st

class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class StationContext:
    __acl__ = [
        (
            Allow,
            TR.Everyone,
            {'read'}
        ),
        (
            Allow,
            TR.Authenticated,
            {'create', 'update'}
        )
    ]

@api_view(['GET'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'read', 
    lambda req: StationContext
)
def station_list(request: ApiRequest, format=None):
    """
    Returns a list of stations
    """

    stations = StationSerializer(Station.objects.all(), many=True)    
    return ApiResponse(stations.data)


@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'create', 
    lambda req: StationContext
)
def station_create(request: ApiRequest, format=None):
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
    lambda req: StationContext
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
