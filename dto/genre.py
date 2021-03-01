class Genre(object):

    def __init__(self,
                 id: str = None,
                 parent: str = None,
                 titles: list = None,
                 detailed: list = None,
                 sub_genres: list = None):
        self.id = id
        self.parent = parent
        self.titles = titles
        self.detailed = detailed
        self.sub_genres = sub_genres
