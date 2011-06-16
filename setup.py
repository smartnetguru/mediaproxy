#!/usr/bin/python

from distutils.core import setup as _setup, Extension
import sys
import re


# Get the title and description from README
readme = open('README').read()
title, description = re.findall(r'^\s*([^\n]+)\s+(.*)$', readme, re.DOTALL)[0]

def get_version():
    return re.search(r"""__version__\s+=\s+(?P<quote>['"])(?P<version>.+?)(?P=quote)""", open('mediaproxy/__init__.py').read()).group('version')


def setup(*args, **kwargs):
    """Mangle setup to ignore media-relay on non-linux platforms"""
    if not sys.platform.startswith('linux2'):
        print "WARNING: skipping the media relay component as this is a non-linux platform"
        kwargs.pop('ext_modules', None)
        kwargs['scripts'].remove('media-relay')
    _setup(*args, **kwargs)


setup(name         = "mediaproxy",
      version      = get_version(),
      author       = "Ruud Klaver",
      author_email = "support@ag-projects.com",
      maintainer   = "AG Projects",
      maintainer_email = "support@ag-projects.com",
      url          = "http://www.ag-projects.com/MediaProxy.html",
      description  = title,
      long_description = description,
      license      = "GPL",
      platforms    = ["Linux"],
      classifiers  = [
          #"Development Status :: 1 - Planning",
          #"Development Status :: 2 - Pre-Alpha",
          #"Development Status :: 3 - Alpha",
          #"Development Status :: 4 - Beta",
          "Development Status :: 5 - Production/Stable",
          #"Development Status :: 6 - Mature",
          #"Development Status :: 7 - Inactive",
          "Intended Audience :: Service Providers",
          "License :: GNU General Public License (GPL)",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Programming Language :: C"
      ],
      packages     = ['mediaproxy', 'mediaproxy.interfaces', 'mediaproxy.interfaces.accounting', 'mediaproxy.interfaces.system'],
      scripts      = ['media-relay', 'media-dispatcher'],
      ext_modules  = [
          Extension(name = 'mediaproxy.interfaces.system._conntrack',
                    sources = ['mediaproxy/interfaces/system/_conntrack.c'],
                    libraries = ["iptc", "netfilter_conntrack"],
                    define_macros = [('MODULE_VERSION', get_version())])
      ]
)

