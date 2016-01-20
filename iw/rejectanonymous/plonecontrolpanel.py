# -*- coding: utf-8 -*-
# Copyright (C) 2008 Ingeniweb

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
"""Patch plone "security" control panel to add a new option
"""
from zope.interface import implementedBy
from zope.interface import classImplementsOnly
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.schema import Bool
from zope.component import getGlobalSiteManager
from zope.formlib.form import FormFields

from plone.app.controlpanel.security import SecurityControlPanel
from plone.app.controlpanel.security import SecurityControlPanelAdapter
from plone.app.controlpanel.security import ISecuritySchema

from iw.rejectanonymous import IPrivateSite


class IPrivateSiteSchema(ISecuritySchema):
    private_site = Bool(
        title=u'Private site',
        description=u"Users must login to view the site. Anonymous users are presented the login form",
        default=False,
        required=False,
    )

# add accessors to adapter


def get_private_site(self):
    return IPrivateSite.providedBy(self.portal)

SecurityControlPanelAdapter.get_private_site = get_private_site


def set_private_site(self, value):
    operator = value and alsoProvides or noLongerProvides
    operator(self.portal, IPrivateSite)

SecurityControlPanelAdapter.set_private_site = set_private_site

SecurityControlPanelAdapter.private_site = property(
    SecurityControlPanelAdapter.get_private_site,
    SecurityControlPanelAdapter.set_private_site
)

# re-register adapter with new interface
_decl = implementedBy(SecurityControlPanelAdapter)
_decl -= ISecuritySchema
_decl += IPrivateSiteSchema
classImplementsOnly(SecurityControlPanelAdapter, _decl.interfaces())
del _decl

getGlobalSiteManager().registerAdapter(SecurityControlPanelAdapter)

# re-instanciate form
SecurityControlPanel.form_fields = FormFields(IPrivateSiteSchema)
