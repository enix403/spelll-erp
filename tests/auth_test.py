from typing import cast

from authzx import *

class TR:
    All = 'sys.all'
    
    Authenticated = 'sys.authn'
    
    @staticmethod
    def AuthRole(role):
        return f'app.authrole:{role}'

    @staticmethod
    def StaffRole(role):
        return f'app.staffrole:{role}'

    @staticmethod
    def BelongsToClg(college_id):
        return f'app.cid:{college_id}'


class AuthRoles:
    STAFF = 'staff'
    ADMIN = 'admin'

class StaffRoles:
    INFO_OFFICER = 'infof'
    DATA_ENTRY = 'dentry'
    PRINCIPAL = 'prncpl'


class StaffResource:
    def __init__(self, college_id):
        self.college_id = college_id
        self.__acl__ = self.create_acl()

    def create_acl(self):
        college_staff = TraitSpec(TR.AuthRole(AuthRoles.STAFF), TR.BelongsToClg(self.college_id))
        admin = TraitSpec(TR.AuthRole(AuthRoles.ADMIN))
        return [
            (
                Allow,
                admin | college_staff,
                {'read'}
            ),
            (
                Allow,
                college_staff & TraitSpec(TR.StaffRole(StaffRoles.DATA_ENTRY)),
                {'create'}
            ),
            (
                Allow,
                admin | (college_staff & TraitSpec(TR.StaffRole(StaffRoles.PRINCIPAL))),
                {'create', 'update'}
            ),
            (
                Allow,
                admin,
                {'delete'}
            )
        ]


class User:
    def __init__(self, authrole, staffrole, college_id):
        self.authrole = authrole
        self.staffrole = staffrole
        self.college_id = college_id

class SimpleTraitCollection(AgentTraitCollection):
    def get_effective_traits(self, agent_handle):
        user = cast(User, agent_handle)

        if user is None:
            return [TR.All]

        if user.authrole == AuthRoles.ADMIN:
            return [
                TR.All,
                TR.Authenticated,
                TR.AuthRole(AuthRoles.ADMIN)
            ]

        return [
            TR.All,
            TR.Authenticated,
            TR.AuthRole(AuthRoles.STAFF),
            TR.StaffRole(user.staffrole),
            TR.BelongsToClg(user.college_id)
        ]


policy = AclAuthorizationPolicy()
def gate(user) -> AuthzGate:
    return AuthzGate(policy, SimpleTraitCollection(user))


def check_user(cid, user, perm):
    return gate(user).allowed(perm, StaffResource(cid))