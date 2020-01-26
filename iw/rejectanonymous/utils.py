from iw.rejectanonymous import IPrivateSite
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


def get_private_site(portal):
    return IPrivateSite.providedBy(portal)


def set_private_site(portal, value):
    operator = value and alsoProvides or noLongerProvides
    operator(portal, IPrivateSite)
