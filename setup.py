from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='pygpg',
      version='1.0',
      description='GnuPG python wrapper.',
      author='Faust',
      author_email='https://www.abnorm.org/contact/',
      url='https://www.abnorm.org/projects/pygpg/',
      download_url='https://www.abnorm.org/projects/pygpg/#downloads',
      license='GNU General Public License v3 or later (GPLv3+)',
      long_description=long_description,
      keywords='gpg GnuPG encrypt sign verify',
      packages=['gpg'],
      classifiers=['Development Status :: 5 - Production/Stable',
'Intended Audience :: Information Technology',
'Intended Audience :: System Administrators',
'Intended Audience :: Developers',
'Intended Audience :: Education',
'Operating System :: OS Independent',
'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
'Programming Language :: Python :: 2.5',
'Programming Language :: Python :: 2.6',
'Programming Language :: Python :: 2.7',
'Programming Language :: Python :: 3',
'Topic :: Security :: Cryptography',
'Topic :: Software Development :: Libraries :: Python Modules',
'Topic :: Utilities',]
     )
