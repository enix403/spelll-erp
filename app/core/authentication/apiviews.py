import datetime
import uuid

import jwt
from rest_framework.decorators import api_view

from app.bootstrap.configmanager import ConfigManager
from app.typehints import ApiRequest, ApiResponse
from app.exceptions import ApiException
from app.models import AppUser

from .token import issue_token, decode_token

def new_access_token(userid):
    return issue_token({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'jti': str(uuid.uuid4()),
        'userid': userid,
        'tk_type': 'acs'
    })


@api_view(['POST'])
def login(request: ApiRequest, format=None) -> ApiResponse:
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
        # use 'ref-' prefix to minimize uuid collision as both uuid's are generated almost at the same time
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
def get_access_token(request: ApiRequest):
    payload = decode_token(request.data.get('refresh_token', ''))
    if payload is None or payload['tk_type'] != 'ref':
        raise ApiException("Invalid refresh token", data={'access': ''})

    access_token = new_access_token(payload['userid'])

    return ApiResponse({
        'type': 'success',
        'msg': 'Token refresh successful',
        'payload': {
            'access': access_token,
        }
    })

