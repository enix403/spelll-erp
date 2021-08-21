from authzx.traits import TraitSpec
from app.core.authentication.traits import TR
from app.core.authentication.roles import AuthRoles, StaffRoles
from app.core.authentication.helpers import ContextGenerator

from authzx.helpers import AclContext

from authzx.actions import Allow


class StationContext(ContextGenerator):
    acl = [
        (
            Allow,
            TR.AuthRole(AuthRoles.Admin),
            {'create', 'read', 'update', 'delete'}
        ),
    ]

    @classmethod
    def generate(cls, request):
        return cls


class CollegeContext(ContextGenerator):
    acl = [
        (
            Allow,
            TR.StaffRole(StaffRoles.Principal),
            {'read'}
        ),
        (
            Allow,
            TR.AuthRole(AuthRoles.Admin),
            {'create', 'read', 'update', 'delete'}
        ),
    ]

    @classmethod
    def generate(cls, request):
        return cls