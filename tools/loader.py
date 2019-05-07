import os
import io
import bson
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from storage.version import LibraryVersion
from storage.group import Group
from wiring import Wiring


def update_version():
    wiring = Wiring()
    path = os.path.join(wiring.settings.LIB_INDEXES, 'version.info')
    with io.open(path) as file:
        num_version = file.read()

    version = LibraryVersion(
        version=num_version.rstrip(),
        added=datetime.now().strftime('%Y%m%d')
    )
    wiring.library_dao.create(version)


def create_group():
    wiring = Wiring()
    default_group = Group(name='default', limit_per_day=10000)
    unlim_group = Group(name='unlim', limit_per_day=9999999)

    wiring.groups.create(default_group)
    wiring.groups.create(unlim_group)


def update_group():
    wiring = Wiring()
    unlim_group = Group(name='unlim', limit_per_day=9999999)
    wiring.groups.update(unlim_group)



# fix_stat()
