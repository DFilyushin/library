class Author(object):

    def __init__(self,
                 id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 middle_name: str = None
                 ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    @property
    def name(self):
        result = '{} {} {}'.format(self.last_name, self.first_name, self.middle_name)
        return result
