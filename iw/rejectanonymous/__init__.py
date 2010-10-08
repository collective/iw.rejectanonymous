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
"""rejectanonymous initialization"""
from zope.interface import Interface
from AccessControl import getSecurityManager

class IPrivateSite(Interface):
    """Marker for sites requiring login"""

from zExceptions import Unauthorized

valid_ids = set(('login_form', 'require_login', 'login.js', 'spinner.gif',
                 'mail_password_form', 'mail_password', 'contact-info',
                 'pwreset_form', 'pwreset_finish'))

valid_subparts = set(('portal_css', 'portal_javascripts', 'passwordreset'))

def isAnonymousUser():
    u = getSecurityManager().getUser()
    return (u is None or u.getUserName() == 'Anonymous User')

def getPortalLogoId(portal):
    props = portal['base_properties']
    return props.getProperty('logoName')

def rejectAnonymous(portal, request):

    if isAnonymousUser():
        url = request.physicalPathFromURL(request['URL'])
        if url[-1] == 'index_html':
            url.pop()
        item_id = url[-1]
        logo_id = getPortalLogoId(portal)

        if url and not (item_id in valid_ids
                        or item_id == logo_id
                        or [path for path in url
                            if path in valid_subparts]):
            raise Unauthorized, "Anonymous rejected"

def insertRejectAnonymousHook(portal, event):
    """ """
    event.request.post_traverse(rejectAnonymous, (portal, event.request))

## try:
##     import plone.add.controlpanel
## except ImportError:
##     pass
## else:
import iw.rejectanonymous.plonecontrolpanel

