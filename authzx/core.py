from typing import Container, Iterable, cast
from authzx.traits import AgentTraitCollection, TraitSpec
from authzx.actions import Allow, Deny

class AuthorizationPolicy:
    def permits(self, permission, resource_context, traits: AgentTraitCollection) -> bool:
        """
            Returns `True` if `permission` is granted according to the given traits and context,
            `False` otherwise
        """

    def all_permissions(self, resource_context, traits: AgentTraitCollection) -> Iterable:
        """
            Returns a list of all permissions granted to the user according to the given traits and context
        """

class AuthzGate:
    def __init__(self, policy: AuthorizationPolicy, traits: AgentTraitCollection):
        self._policy = policy
        self._traits = traits

    def get_policy(self):
        return self._policy

    def get_traits(self):
        return self._traits

    def allowed(self, perm, context):
        return self._policy.permits(perm, context, self._traits)

    def allowed_one(self, perms, context):
        for perm in perms:
            if self._policy.permits(perm, context, self._traits):
                return True

        return False

    def allowed_all(self, perms, context):
        for perm in perms:
            if not self._policy.permits(perm, context, self._traits):
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
        try:
            acl = resource_context.acl
        except AttributeError:
            return False

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

    def all_permissions(self, resource_context, agent_traits: AgentTraitCollection):
        try:
            acl = resource_context.acl
        except AttributeError:
            return []

        all_perms = set()

        for (action, trait, perms) in acl:
            assert (action is Allow or action is Deny), f"Invalid action: {action}"
            if isinstance(trait, TraitSpec):
                passed = _resolve_control(trait, agent_traits)
            else:
                passed = agent_traits.has_trait(trait)

            if passed:
                if action == Allow:
                    all_perms.update(perms)
                else:
                    all_perms.difference_update(perms)
            
        return all_perms