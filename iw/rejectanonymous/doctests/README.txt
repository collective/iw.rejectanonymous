==========================
iw.rejectanonymous testing
==========================

How to use iw.rejectanonymous ?
===============================

By default an anonymous user can browse portal:

    >>> portal_url = self.portal.absolute_url()
    >>> browser.open(portal_url)
    >>> browser.url == portal_url
    True
    >>> browser.headers['status'].upper()
    '200 OK'

We mark the portal with ``IPrivateSite``; this can be achieved by code or in the
ZMI using "Interfaces" tab on the portal object. Now Anonymous will get
Unauthorized exception. In a plone site this should results in a redirect to
login form.

.. admonition::
   Security control panel

   The Plone "Security" control panel has now a new **Private site** option for
   this. A site manager does not need to go in ZMI.

Marking the site as private.

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
    >>> logo_url = self.portal.absolute_url() + '/' + logo_id
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

Then we log in, and we will be authorized to browse the portal.

    >>> from Products.PloneTestCase.setup import default_user, default_password
    >>> browser.open(login_form_url)
    >>> browser.getControl(name='__ac_name').value = default_user
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name="submit").click()
    >>> browser.open(portal_url)
    >>> browser.url == portal_url
    True
    >>> browser.headers['status'].upper()
    '200 OK'

Customizing
===========

The default setup of authorized resources are exhaustive for a vanilla Plone
site, but some sites that are customized in depths, particularly with a
dedicated theme may need to publish other resources in the pages available to
the anonymous user, or an additional page (disclaimer, ...) linked from the
login page.

Your policy or theme component may use the ``iw.rejectanonymous.addValidIds`` to
enable new object ids to be published, and
``iw.rejectanonymous.addValidSubparts`` to add traversed resources available to
the anonymous user. The only argument required by these two functions is a
single string to add one id or subpart or a sequence of string of such ids or
subparts.

First we logout to verify this.

    >>> browser.open(portal_url + '/logout')
    Traceback (most recent call last):
    ...
    Unauthorized: ...

Suppose our theme shows the ``user.gif`` and ``add_icon.gif`` icons for some
reason. The standard setup of ``iw.rejectanonymous`` does not enable this and
your page will not show as expected to the anonymous user.

    >>> browser.open(portal_url + '/user.gif')
    Traceback (most recent call last):
    ...
    Unauthorized: ...
    >>> browser.open(portal_url + '/add_icon.gif')
    Traceback (most recent call last):
    ...
    Unauthorized: ...

Now let's add our resources to valid ids using our customisation API.

    >>> from iw.rejectanonymous import addValidIds
    >>> addValidIds('user.gif', 'add_icon.gif')

And let's check the anonymous can get these resources.

    >>> browser.open(portal_url + '/user.gif')
    >>> browser.url
    'http://nohost/plone/user.gif'
    >>> browser.headers['status'].upper()
    '200 OK'
    >>> browser.open(portal_url + '/add_icon.gif')
    >>> browser.url
    'http://nohost/plone/add_icon.gif'
    >>> browser.headers['status'].upper()
    '200 OK'

If the custom pages available to the anonymous user require KSS, those KSS
resources cannot actually be published with the special tests setup.

    >>> cooked_kss = self.portal.portal_kss.getCookedResources()[0]
    >>> cooked_kss_url = '%s/portal_kss/%s' % (portal_url, cooked_kss.getId())
    >>> browser.open(cooked_kss_url)
    Traceback (most recent call last):
    ...
    Unauthorized: ...

Now let's add our subpart to the valid ones through our customisation API.

    >>> from iw.rejectanonymous import addValidSubparts
    >>> addValidSubparts('portal_kss')

And let's check we can now publish KSS resources to anonymous users.

    >>> browser.open(cooked_kss_url)
    >>> browser.url == cooked_kss_url
    True
    >>> browser.headers['status'].upper()
    '200 OK'

