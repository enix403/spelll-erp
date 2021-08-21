from typing import Any, ClassVar, Optional, Type
from functools import wraps

from authzx.core import AclAuthorizationPolicy, AuthorizationPolicy, AuthzGate

from app.exceptions import ApiException
from app.typehints import ApiRequest
from app.models.auth import AppUser
from app.utils import httpcodes, to_int

from .helpers import ContextGenerator
from .token import decode_token
from .traits import SimpleTraitCollection

class PermissionGate:
    _authz_policy: ClassVar[AuthorizationPolicy]
    _exception_obj: ClassVar[Exception]

    def __init__(self, request):
        self.user = self._load_user(request)
        self._gate = AuthzGate(self._authz_policy, SimpleTraitCollection(self.user))

    def get_user(self):
        return self.user

    def all_permissions(self, context):
        return self._gate.get_policy().all_permissions(context, self._gate.get_traits())

    def _load_user(self, request) -> Optional[AppUser]:
        """ Load and return the user object from database or return None if not authenticated"""

    def require(self, perm, context):
        if not self._gate.allowed(perm, context):
            raise self._exception_obj

    def require_one(self, perms, context):
        if not self._gate.allowed_one(perms, context):
            raise self._exception_obj

    def require_all(self, perms, context):
        if not self._gate.allowed_all(perms, context):
            raise self._exception_obj


class ApiPermissionGate(PermissionGate):
    _authz_policy = AclAuthorizationPolicy()
    _exception_obj = ApiException("Permission Denied", code=httpcodes.HTTP_403_FORBIDDEN)

    _TOKEN_PREFIX = 'Bearer'

    @classmethod
    def get_token(cls, header: str):
        bearer, _, token = header.partition(' ')
        if bearer != cls._TOKEN_PREFIX:
            return ''

        return token


    def _load_user(self, request: ApiRequest) -> Optional[AppUser]:
        payload = decode_token(self.get_token(request.META.get('HTTP_AUTHORIZATION', '')))
        if payload is None:
            return None

        if payload['tk_type'] != 'acs':
            return None

        userid: int = to_int(payload.get('userid', 0))

        try:
            return AppUser.objects.filter(pk=userid).get()
        except AppUser.DoesNotExist:
            return None



def require(gate: Type[PermissionGate], perm: str, context_gen: ContextGenerator):
    def wrapper(func):
        @wraps(func)
        def _f(request, *args, **kwargs):
            gate(request).require(perm, context_gen.generate(request))
            return func(request, *args, **kwargs)

        return _f

    return wrapper


def require_all(gate: Type[PermissionGate], perms: str, context_gen: ContextGenerator):
    def wrapper(func):
        @wraps(func)
        def _f(request, *args, **kwargs):
            gate(request).require_all(perms, context_gen.generate(request))
            return func(request, *args, **kwargs)

        return _f

    return wrapper


def require_one(gate: Type[PermissionGate], perms: str, context_gen: ContextGenerator):
    def wrapper(func):
        @wraps(func)
        def _f(request, *args, **kwargs):
            gate(request).require_one(perms, context_gen.generate(request))
            return func(request, *args, **kwargs)

        return _f

    return wrapper
