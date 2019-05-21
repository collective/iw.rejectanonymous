import os
from setuptools import setup, find_packages

def read(*names):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, *names)
    return open(path, 'r').read().strip()

version = '1.2.4'

setup(name='iw.rejectanonymous',
      version=version,
      description="Disallow access to a Plone site and its children if user is anonymous",
      long_description=(read('README.rst')
                        + '\n\n'
                        + read('CHANGES.rst')),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.2",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Zope2",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='plone extranet',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='https://svn.plone.org/svn/collective/iw.rejectanonymous',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['iw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """
      )
