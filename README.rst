==================
iw.rejectanonymous
==================


What is iw.rejectanonymous ?
============================

This package is made to reject unconditionnally anonymous users from a Plone
site, without any change in your security policy matrix or workflows. They
should get redirected by plone to login form. The basic use case is an extranet,
where all visitors must be authenticated.

Works with
==========

Plone 3, 4, 5

Installation
============

Add ``iw.rejectanonymous`` to the ``eggs`` option of your
``plone.recipe.zope2instance`` part ::

  ...
  [instance]
  recipe = plone.recipe.zope2instance
  ...
  eggs =
      ...
      iw.rejectanonymous
      ...
  ...
  # The ZCML slug is no more required with Plone 3.3 and up
  zcml =
      ...
      iw.rejectanonymous
      ...

Re-run buildout, then open the "Security" control panel of any Plone site of
your instance. A new **Private site** checkbox lets you (de)activate
``iw.rejectanonymous``.

Customization
=============

``iw.rejectanonymous`` enables the publication of some resources to the
anonymous user, more specifically to enable all media and resources required
from the standard loging page and the password reset page.

Adding valid ids
----------------

If your customized logging page requires some specific images or your site
policy component provides a signup page which name is not ``login_form`` you may
add additional ids (url last part) that are available to anonymous users.

::

  from iw.rejectanonymous import addValidIds
  ...
  addValidIds('some_image.png', 'my_login_form')


Adding valid subparts
---------------------

If you want to let anonymous users browse the pages of some folders, you need to
add valid subparts.

::

  from iw.rejectanonymous import addValidSubparts
  ...
  addValidSubparts('disclaimer', 'public_section')

Adding valid subparts prefixes
------------------------------

If you want to let anonymous users browse the pages of some folders with
specific prefixes, you need to add valid subpart prefixes.

::

  from iw.rejectanonymous import addValidSubpartPrefixes
  ...
  addValidSubpartPrefixes('public_')

Hiding viewlets
---------------

You may hide viewlets from the views of the site (login form, password reset
form). You need for this to add such lines in your site policy ZCML.

::

  <browser:viewlet
    name="original.viewlet.name"
    for="iw.rejectanonymous.IPrivateSite"
    manager="original.viewlet.manager.Interface"
    class="original.viewlet.Class"
    permission="cmf.SetOwnProperties"
  />

``name``
  Keep the original viewlet name.

``for``
  ``iw.rejectanonymous.IPrivateSite`` the marker interface set to private sites

``manager``
  Keep the original manager

``class``
  Keep the original viewlet class

``permission``
  Choose a permission that is not granted to an anonymous user but to anyone
  else. ``cmf.SetOwnProperties`` is a good choice if your site has the standard
  security policy.

See how we hide the ``plone.personal_bar`` and the ``plone.searchbox`` in the
``configure.zcml`` of this component.

Links
=====

Cheeseshop
  http://pypi.python.org/pypi/iw.rejectanonymous

Git repository
  https://github.com/collective/iw.rejectanonymous

Issue tracker
  https://github.com/collective/iw.rejectanonymous/issues

Old SVN repository (up to 1.0.2)
  https://svn.plone.org/svn/collective/iw.rejectanonymous

Contributors
============

* Bertrand Mathieu
* Thomas Desvenain
* Gilles Lenfant
* Elisabeth Leddy
