# -*- coding: utf-8 -*-
# Copyright (C)2007 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
""" defines a test class and its Plone Site layer for plone tests
"""
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.Five import zcml
from Products.Five import fiveconfigure

@onsetup
def setup_reject_anonymous_site():
    """
    """
    import iw.rejectanonymous
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', iw.rejectanonymous)
    fiveconfigure.debug_mode = False

setup_reject_anonymous_site()
ptc.setupPloneSite()

class TestCase(ptc.FunctionalTestCase):
    """test case used in tests"""
