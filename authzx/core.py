from typing import Container, cast
from authzx.traits import AgentTraitCollection, TraitSpec
from authzx.actions import Allow, Deny

class AuthorizationPolicy:
    def permits(self, permission, resource_context, traits: AgentTraitCollection) -> bool:
        """
            Returns `True` if `permission` is granted according to the given traits and context,
            `False` otherwise
        """

class AuthzGate:
    def __init__(self, policy: AuthorizationPolicy, traits: AgentTraitCollection):
        self.policy = policy
        self.traits = traits

    def allowed(self, perm, context):
        return self.policy.permits(perm, context, self.traits)

    def allowed_one(self, perms, context):
        for perm in perms:
            if self.policy.permits(perm, context, self.traits):
                return True

        return False

    def allowed_all(self, perms, context):
        for perm in perms:
            if not self.policy.permits(perm, context, self.traits):
                return False

        return True
        

def _resolve_control(root_node: TraitSpec, traits: AgentTraitCollection):
    resolved = root_node.connector == TraitSpec.OPER_AND
    for child in root_node.children:
        if isinstance(child, TraitSpec):
            resolve_child = _resolve_control(child, traits)
        else:
            resolve_child = traits.has_trait(child)

        if root_node.connector == TraitSpec.OPER_AND:
            if not resolve_child:
                resolved = False
                break

        else:
            if resolve_child:
                resolved = True
                break

    if root_node.negated:
        resolved = not resolved

    return resolved

class AclAuthorizationPolicy(AuthorizationPolicy):
    def permits(self, required_permission, resource_context, agent_traits: AgentTraitCollection):
        acl = []
        try:
            acl = resource_context.__acl__
        except AttributeError:
            return False

        if callable(acl):
            acl = acl()

        allowed = False

        for (action, trait, perms) in acl:
            assert (action is Allow or action is Deny), f"Invalid action: {action}"
            perms = cast(Container, perms)
            if required_permission in perms:
                if isinstance(trait, TraitSpec):
                    passed = _resolve_control(trait, agent_traits)
                else:
                   passed = agent_traits.has_trait(trait) 
                
                if passed:
                    allowed = action is Allow

        return allowed