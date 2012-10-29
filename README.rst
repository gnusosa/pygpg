==========
pygpg
==========

`https://www.abnorm.org/projects/pygpg/ <https://www.abnorm.org/projects/pygpg/>`_

GnuPG python wrapper.

This simple module implements some function which will let you:

* Encrypt messages or files
* Sign massages or files (also supporting clear sign and detached sign)
* Verify signs
* Export public keys
* Import public keys (also supporting custom keyserver)
* Deleting public and private keys
* Listing public and private keys

Requirements
^^^^^^^^^^^^
* GnuPG

Install
^^^^^^^
Gentoo users:
-------------
You should first enable the `Abnorm Overlay <https://www.abnorm.org/portage/>`_ then you can install it::

	emerge pygpg

Using pip:
----------
::

	pip install pygpg

Manual installation and git installation:
-----------------------------------------
To manually install last stable release or older releases `dowload <https://github.com/faust/pygpg/downloads>`_ the tarball
and extract it::

	$ tar xzvvf pygpg-*.tar.gz
	$ cd pygpg-*
	$ sudo python setup.py install

To install from git please run::

	$ git clone https://github.com/faust/pygpg.git
	$ cd pygpg
	$ sudo python setup.py install

Licensing
^^^^^^^^^
tcpextract is released under `GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>`_ or later.

Contact
^^^^^^^
You can contact the Author using `this form  <https://www.abnorm.org/contact/>`_
