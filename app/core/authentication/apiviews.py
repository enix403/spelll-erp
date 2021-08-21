from app.core.sections.context import SectionContext
from app.core.manage.context import CollegeContext, StationContext
import datetime
import uuid
from typing import cast

from rest_framework.decorators import api_view

from app.models import College
from authzx.helpers import make_ctx_require_all_traits
from app.core.authentication.traits import TR
from app.typehints import ApiRequest, ApiResponse
from app.exceptions import ApiException
from app.models import AppUser

from . import permissions
from .token import issue_token, decode_token

def new_access_token(userid):
    return issue_token({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45),
        'jti': str(uuid.uuid4()),
        'userid': userid,
        'tk_type': 'acs'
    })


@api_view(['POST'])
def login(request: ApiRequest) -> ApiResponse:
    username = request.data.get('username', None)
    password = request.data.get('password', None)

    failure_exp = ApiException("Invalid username or password", data={'access': '', 'refresh': ''})

    if not username or not password:
        raise failure_exp

    try:
        user = AppUser.objects.filter(username=username).get()
    except AppUser.DoesNotExist:
        raise failure_exp

    if not user.verify_password(password):
        raise failure_exp

    access_token = new_access_token(user.pk)

    ref_token = issue_token({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=20),
        'jti': f'ref-{str(uuid.uuid4())}',
        'userid': user.pk,
        'tk_type': 'ref',
    })

    return ApiResponse({
        'type': 'success',
        'msg': 'Login successful',
        'payload': {
            'access': access_token,
            'refresh': ref_token 
        }
    })


@api_view(['POST'])
def get_access_token(request: ApiRequest) -> ApiResponse:
    payload = decode_token(request.data.get('refresh_token', ''))
    if payload is None or payload['tk_type'] != 'ref':
        raise ApiException("Invalid refresh token. Please login again", data={'access': ''})

    access_token = new_access_token(payload['userid'])

    return ApiResponse({
        'type': 'success',
        'msg': 'Token refresh successful',
        'payload': {
            'access': access_token,
        }
    })


_authenticated_context = make_ctx_require_all_traits(TR.Authenticated)
@api_view(['GET'])
def get_user_info(request: ApiRequest) -> ApiResponse:
    gate = permissions.ApiPermissionGate(request)
    gate.require('access', _authenticated_context)

    user = cast(AppUser, gate.get_user())
    try:
        college = College.objects.filter(pk=user.college_id).get()
        clg_name = college.name
        clg_id = college.pk
    except:
        clg_name = ''
        clg_id = None


    return ApiResponse({
        'type': 'success',
        'msg': '',
        'payload': {
            'info': {
                'name': user.name,
                'username': user.username,
                'authrole': user.auth_role,
                'staffrole': user.staff_role,
                'college': {
                    'id': clg_id,
                    'name': clg_name,
                }
            },
            'permissions': {
                'colleges': gate.all_permissions(CollegeContext.generate(request)),
                'station': gate.all_permissions(StationContext.generate(request)),
                'sections': gate.all_permissions(SectionContext(user.college_id).generate(None))
            }
        }
    })
