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
from Acquisition import aq_get
from zExceptions import Unauthorized

try:
    from plone import restapi
    HAS_RESTAPI = True
except ImportError:
    HAS_RESTAPI = False


class IPrivateSite(Interface):
    """Marker for sites requiring login"""


valid_ids = frozenset((
    'login_form', 'require_login', 'login.js', 'spinner.gif',
    'mail_password_form', 'mail_password', 'contact-info', 'pwreset_form',
    'pwreset_finish', 'favicon.ico', 'logo.jpg', 'logo.png'
    ))

if HAS_RESTAPI:
    valid_ids = valid_ids.union(('reset-password', '@login', '@login-renew', '@logout'))


valid_subparts = frozenset((
    'portal_css', 'portal_javascripts', 'passwordreset', 'portal_kss'
    ))

valid_subpart_prefixes = frozenset(('++resource++', '++theme++'))

# Customization functions
def addValidIds(*new_ids):
    """A customized Plone site may need to publish other ids as resources
    of the login process. The policy or third party component just need to
    use this function for this to happen.

    :param new_ids: one or more ids
    """
    global valid_ids
    valid_ids |= set(new_ids)
    return

def addValidSubparts(*new_subparts):
    """A customized Plone site may need to publish other subparts for resources
    of the login process. The policy or third party component just need to
    use this function for this to happen.

    :param new_subparts: one or more traversal ids
    """
    global valid_subparts
    valid_subparts |= set(new_subparts)
    return

def addValidSubpartPrefixes(*new_prefixes):
    """A customized Plone site may need to publish other subpart prefixes for
    resources of the login process. The policy or third party component just
    need to use this function for this to happen.

    :param new_subparts: one or more traversal ids
    """
    global valid_subpart_prefixes
    valid_subpart_prefixes |= set(new_prefixes)

# Utilities
def isAnonymousUser():
    u = getSecurityManager().getUser()
    return (u is None or u.getUserName() == 'Anonymous User')

def getPortalLogoId(portal):
    props = aq_get(portal, 'base_properties', None)
    return props is not None and props.getProperty('logoName', '') or ''

def rejectAnonymous(portal, request):
    if request['REQUEST_METHOD'] == 'OPTIONS':
        return
    if isAnonymousUser():
        url = request.physicalPathFromURL(request['URL'])
        if url[-1] == 'index_html':
            url.pop()
        item_id = url[-1]
        logo_id = getPortalLogoId(portal)

        if url and not (
            item_id in valid_ids
            or item_id == logo_id
            or [path for path in url
                if path in valid_subparts]
            or [path for path in url
                if [v for v in valid_subpart_prefixes if path.startswith(v)]]
                ):
            raise Unauthorized, "Anonymous rejected"

def insertRejectAnonymousHook(portal, event):
    """ """
    try:
        event.request.post_traverse(rejectAnonymous, (portal, event.request))
    except RuntimeError:
        # Make this work in a testrunner
        pass

import iw.rejectanonymous.plonecontrolpanel

