# -*- coding: utf-8 -*-
#
# Copyright (C)2006-2009 Edgewall Software
# Copyright (C) 2006 Matthew Good <trac@matt-good.net>
# Copyright (C) 2006 Christopher Lenz <cmlenz@gmx.de>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.

"""Various classes and functions to provide some backwards-compatibility with
previous versions of Python from 2.6 onward.
"""

import math
import os
import time

from trac.util.text import cleandoc

# Windows doesn't have a crypt module by default.
try:
    from crypt import crypt
except ImportError:
    try:
        from passlib.hash import des_crypt
    except ImportError:
        crypt = None
    else:
        def crypt(secret, salt):
            return des_crypt.encrypt(secret, salt=salt)

# Import symbols previously defined here, kept around so that plugins importing
# them don't suddenly stop working
all = all
any = any
frozenset = frozenset
reversed = reversed
set = set
sorted = sorted
from collections import OrderedDict
from functools import partial
from hashlib import md5, sha1
from itertools import groupby, tee


def rpartition(s, sep):
    return s.rpartition(sep)

# An error is raised by subprocess if we ever pass close_fds=True on Windows.
# We want it to be True on all other platforms to not leak file descriptors.
close_fds = os.name != 'nt'


def wait_for_file_mtime_change(filename):
    """This function is typically called before a file save operation,
    waiting if necessary for the file modification time to change. The
    purpose is to avoid successive file updates going undetected by the
    caching mechanism that depends on a change in the file modification
    time to know when the file should be reparsed."""

    from trac.util import touch_file
    try:
        mtime = os.stat(filename).st_mtime
        touch_file(filename)
        while mtime == os.stat(filename).st_mtime:
            time.sleep(1e-3)
            touch_file(filename)
    except OSError:
        pass  # file doesn't exist (yet)
