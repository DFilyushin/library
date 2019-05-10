from datetime import datetime
from wiring import Wiring
from storage.group import Group, GroupExist


def create_group(wiring: Wiring):

    print('{}: Creating standard groups...'.format(datetime.now()))

    groups = list()
    groups.append(Group(name='default', limit_per_day=10000))
    groups.append(Group(name='unlim', limit_per_day=9999999))

    try:
        for group in groups:
            wiring.groups.create(group)
    except GroupExist:
        print('Group {} already exists'.format(group.name))

    print('{}: Done...'.format(datetime.now()))
