import os
import io
from datetime import datetime
from wiring import Wiring
from dto.version import LibraryVersion


def update_version(wiring: Wiring):
    print('{}: Update version of library'.format(datetime.now()))
    path = os.path.join(wiring.settings.LIB_INDEXES, 'version.info')
    try:
        with io.open(path) as file:
            num_version = file.read()
    except FileNotFoundError:
        print('File {} not found!'.format(path))

    version = LibraryVersion(
        version=num_version.rstrip(),
        added=datetime.now().strftime('%Y%m%d')
    )
    wiring.library_dao.create(version)

    print('{}: Done'.format(datetime.now()))
