import os
from setuptools import setup, find_packages

version = '1.0.2dev'

README = os.path.join(os.path.dirname(__file__),
                      'iw', 'rejectanonymous', 'docs', 'README.txt')
long_description = open(README, 'r').read() + '\n\n'

setup(name='iw.rejectanonymous',
      version=version,
      description="Disallow access to a folder and its children if user is anonymous",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
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
      """,
      )
