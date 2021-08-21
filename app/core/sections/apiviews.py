from app.core.manage.context import StationContext
from app.core.sections.context import SectionContext
import app.utils as utils
from app.models import College, Section

from rest_framework import serializers
from rest_framework.decorators import api_view

from app.core.authentication import permissions
from app.exceptions import ApiException, ApiExceptionNotFound
from app.typehints import ApiRequest, ApiResponse
from app.models import Station

class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

_global_section_context_gen = SectionContext()

def make_section(name, college: College):
    sec = Section()
    sec.name = name
    sec.college = college
    sec.save()
    return sec

# ======================================================================================
# ====================================== SECTIONS ======================================
# ======================================================================================

@api_view(['GET'])
def section_list(request: ApiRequest, college_id: int):
    """
    Returns a list of sections
    """
    permissions.ApiPermissionGate(request).require('read', SectionContext(college_id).generate(None))

    sections = SectionSerializer(Section.objects.filter(college_id=college_id), many=True)    
    return ApiResponse(sections.data)

@api_view(['POST'])
@permissions.require(
    permissions.ApiPermissionGate, 
    'create', 
    _global_section_context_gen
)
def section_create(request: ApiRequest):

    name = request.data.get('name', '').strip()
    college_id = utils.to_int(request.data.get('college_id', 0))

    data = {'created_id': None, 'created_name': '', 'created_college_id': None}

    if not name:
        raise ApiException("Invalid name", data=data)

    if Section.objects.filter(name=name, college_id=college_id).exists():
        raise ApiException(f'Section \'{name}\' already exists', data=data)

    try:
        college = College.objects.filter(pk=college_id).get()
    except College.DoesNotExist:
        raise ApiException("College not found", data=data)


    clg = make_section(name, college)
    data['created_id'] = clg.pk
    data['created_name'] = name
    data['created_college_id'] = college.pk

    return ApiResponse({
        'type': 'success',
        'msg': f'Section \'{name}\' created successfully',
        'payload': data
    })


@api_view(['POST'])
def section_update(request: ApiRequest, section_id: int):

    try:
        section = Section.objects.filter(pk=section_id).get()
    except Section.DoesNotExist:
        raise ApiExceptionNotFound()

    college_id = section.college_id

    permissions.ApiPermissionGate(request).require('update', SectionContext(college_id).generate())

    name = request.data.get('name', '').strip()

    data = {'updated_id': None, 'updated_name': '', 'updated_college_id': None}

    if not name:
        raise ApiException("Invalid name", data=data)

    if Section.objects.filter(name=name, college_id=college_id).exists():
        raise ApiException(f'Section \'{name}\' already exists', data=data)

    updated_count = Section.objects.filter(pk=section_id).update(name=name)

    if updated_count == 0:
        raise ApiExceptionNotFound()

    data['updated_id'] = section_id
    data['updated_name'] = name
    data['updated_college_id'] = college_id

    return ApiResponse({
        'type': 'success',
        'msg': f'Section updated successfully',
        'payload': data
    })