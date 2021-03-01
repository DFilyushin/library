class User(object):

    def __init__(self,
                 id: str = None,
                 login: str = None,
                 password: str = None,
                 group: str = 'default'
                 ):
        self.id = id
        self.login = login
        self.password = password
        self.group = group
