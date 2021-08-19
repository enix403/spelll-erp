from app.utils import AclContext
from authzx.actions import Allow

from rest_framework import serializers
from rest_framework.decorators import api_view

from app.core.authentication.traits import TR
from app.core.authentication.helpers import ContextGenerator
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

class StationContext(ContextGenerator):
    acl = [
        (
            Allow,
            TR.Authenticated,
            {'read'}
        ),
        (
            Allow,
            TR.Authenticated,
            {'create', 'update'}
        )
    ]

    @classmethod
    def generate(cls, request):
        return cls

_global_station_context_gen = StationContext()

@api_view(['GET'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'read', 
    _global_station_context_gen
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
    _global_station_context_gen
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
