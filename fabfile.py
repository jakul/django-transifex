import os
from fabric.utils import puts
import random
import string
import sys
from fabric.operations import local
try:
    import readline # This module gives line editing and history
except ImportError:
    pass

_PYPI_UPLOAD_COMMAND = 'python setup.py sdist upload'


def upload_to_pypi():
    _ensure_can_hardlink()
    local(_PYPI_UPLOAD_COMMAND)

def _ensure_can_hardlink():
    new_filename = '.' + ''.join(random.sample(string.letters, 20))
    try:
        os.link('fabfile.py', new_filename)
    except OSError:
        puts('Operating system does not support hardlinking in this folder')
        sys.exit(1)
    else:
        os.remove(new_filename)
