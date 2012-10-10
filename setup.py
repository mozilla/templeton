# This Source Code is subject to the terms of the Mozilla Public License
# version 2.0 (the "License"). You can obtain a copy of the License at
# http://mozilla.org/MPL/2.0/.

import sys
from setuptools import setup

version = '0.6.1'

deps = ['web.py', 'tempita', 'python-daemon', 'which']

if sys.version < '2.5' or sys.version >= '3.0':
    print >>sys.stderr, '%s requires Python >= 2.5 and < 3.0' % _PACKAGE_NAME
    sys.exit(1)

try:
    import json
except ImportError:
    deps.append('simplejson')

setup(name='templeton',
      version=version,
      description="Minimal web framework for rapid development of web tools",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Mark Cote',
      author_email='mcote@mozilla.com',
      url='https://github.com/markrcote/templeton',
      license='MPL',
      scripts=['scripts/templeton',
               'scripts/templetond',
               'scripts/templeton.fcgi'],
      packages=['templeton'],
      package_data={'templeton': ['templates/project/html/*',
                                  'templates/project/server/*',
                                  'templates/server/*',
                                  'server/scripts/*',
                                  'server/style/*css',
                                  'server/style/Aristo/*css',
                                  'server/style/Aristo/images/*']},
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      )
