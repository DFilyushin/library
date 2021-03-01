class Group(object):

    def __init__(self, id: str = None, name: str = None, limit_per_day: int = 0):
        self.id = id
        self.name = name
        self.limit_per_day = limit_per_day
