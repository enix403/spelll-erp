from authzx.traits import AgentTraitCollection

class TR:
    Everyone = 'sys.Everyone'
    Authenticated = 'sys.authncd'

class SimpleTraitCollection(AgentTraitCollection):
    def get_effective_traits(self, agent_handle):
        if agent_handle is None:
            return [TR.Everyone]

        return [
            TR.Everyone,
            TR.Authenticated
        ]


