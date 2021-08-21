import dataclasses
from typing import Union
from authzx.actions import Allow
from app.core.authentication.roles import AuthRoles, StaffRoles
from authzx.traits import TraitSpec
from app.core.authentication.traits import TR
from authzx.helpers import AclContext
from app.core.authentication.helpers import ContextGenerator
from app.typehints import ApiRequest

class SectionContext(ContextGenerator):

    def __init__(self, college_id=None):
        self.college_id = college_id

    def generate(self, request_payload = None):
        if self.college_id is None:
            college_id = request_payload.data.get('college_id', 0)
        else:
            college_id = self.college_id

        belongs_to_college = TraitSpec(TR.BelongsToCollege(college_id))
        is_admin = TraitSpec(TR.AuthRole(AuthRoles.Admin))

        return AclContext([
            (
                Allow,
                is_admin | belongs_to_college,
                {'read'}
            ),
            (
                Allow,
                TraitSpec(TR.StaffRole(StaffRoles.Principal)) & belongs_to_college,
                {'create'}
            ),
            (
                Allow,
                is_admin,
                {'create', 'update', 'delete'}
            )
        ])