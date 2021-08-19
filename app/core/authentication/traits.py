from authzx.traits import AgentTraitCollection

class TR:
    Everyone = 'sys.Everyone'
    Authenticated = 'sys.authncd'

    @staticmethod
    def BelongsToCollege(college_id):
        return f'app.ClgID({college_id})'

class SimpleTraitCollection(AgentTraitCollection):
    def get_effective_traits(self, agent_handle):
        if agent_handle is None:
            return [TR.Everyone]

        return [
            TR.Everyone,
            TR.Authenticated
        ]


