==========================
iw.rejectanonymous package
==========================

.. contents::

What is iw.rejectanonymous ?
============================

This package is made to reject unconditionnally anonymous users from a plone
site; they should get redirected by plone to login form. The basic use case is
an extranet, where all visitors must be authenticated.

How to use iw.rejectanonymous ?
===============================

By default an anonymous user can browse portal:

    >>> portal_url = self.portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.url == portal_url
    True
    >>> browser.headers['status']
    '200 OK'

We mark the portal with IPrivateSite; this can be achieved by code or in the ZMI
using "Interfaces" tab on the portal object. Now Anonymous will get Unauthorized
exception. In a plone site this should results in a redirect to login form.

    >>> from zope.interface import alsoProvides
    >>> from iw.rejectanonymous import IPrivateSite
    >>> alsoProvides(self.portal, IPrivateSite)
    >>> browser.open(portal_url)
    Traceback (most recent call last):
    ...
    Unauthorized: ...

Login form and some styles resources are still accessible:

    >>> login_form_url = self.portal.login_form.absolute_url()
    >>> browser.open(login_form_url)
    >>> browser.url == login_form_url
    True
    >>> require_login_url = self.portal.require_login.absolute_url()
    >>> browser.open(require_login_url)
    >>> browser.url == require_login_url
    True
    >>> cooked_css = self.portal.portal_css.getCookedResources()[0]
    >>> cooked_css_url = '%s/portal_css/%s' % (portal_url, cooked_css.getId())
    >>> browser.open(cooked_css_url)
    >>> browser.url == cooked_css_url
    True
    >>> cooked_js = self.portal.portal_javascripts.getCookedResources()[0]
    >>> cooked_js_url = '%s/portal_javascripts/%s' % (portal_url, cooked_js.getId())
    >>> browser.open(cooked_js_url)
    >>> browser.url == cooked_js_url
    True
    >>> logo_id = self.portal.base_properties.getProperty('logoName')
    >>> logo_url = self.portal[logo_id].absolute_url()
    >>> browser.open(logo_url)
    >>> browser.url == logo_url
    True
    >>> mail_password_form_url = self.portal.mail_password_form.absolute_url()
    >>> browser.open(mail_password_form_url)
    >>> browser.url == mail_password_form_url
    True

Reset password tool is accessible as well.

    >>> passwordreset_url = self.portal.passwordreset.absolute_url()
    >>> browser.open(passwordreset_url)
    >>> browser.url == passwordreset_url
    True

Then we log in, and we will be authorized to browse the portal

    >>> from Products.PloneTestCase.setup import default_user, default_password
    >>> browser.addHeader('Authorization',
    ...                   'Basic %s:%s' % (default_user, default_password))
    >>> browser.open(portal_url)
    >>> browser.url == portal_url
    True
    >>> browser.headers['status']
    '200 OK'
    
