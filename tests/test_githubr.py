# -*- coding: utf-8 eval: (blacken-mode 1) -*-
#
# September 4 2021, Christian Hopps <chopps@gmail.com>
#
# Copyright (c) 2021 by Christian E. Hopps.
# All rights reserved.
#
# See LICENSE file in the project root directory for license terms,
# otherwise assume you have no license to the code.
#
from githubr import __version__


def test_version():
    assert __version__ == '0.1.0'
