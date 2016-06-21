wundertool-py
==============
Tool for working with `Docker <https://www.docker.com/>`_ containers.

Mission statement:

1. Provide a simplified and unified tool for all the members of the team.
2. Provide additional functionality to existing tools.
3. Include everything from developing to packaging and deploying code in one tool.
3. Allow the project team to easily define the whole stack of software required for the project that is used everywhere from local development to production.

Requirements:

- docker
- python 3 or later

Installation
------------
You can always install the tool from PyPI with::

  pip install wundertool

*Note: OS X doesn't have python 3 or pip installed by default. You should install them with `brew` first and then install `wundertool`*::

  brew install python3
  pip3 install wundertool

Upgrade
-------
Upgrade to the latest version with::

  pip install wundertool --upgrade

or on OS X with python 3::

  pip3 install wundertool --upgrade

Usage
-----
Currently available commands are mostly equivalent of those of docker-compose. See this for list of available commands::

  wundertool commands

Development
-----------
Requirements:

- python 3.4 or later

You can clone this module locally and install it in development mode in an virtual environment like this::

  git clone https://github.com/wunderkraut/wundertool-py.git
  cd wundertool-py
  git submodule init
  git submodule update
  pyvenv .
  source bin/activate
  pip install -e ".[dev]"

You always need to activate the wundertool-py virtual environment when opening a new terminal for development::

  source <DIR>/wundertool-py/bin/activate

Submodule upstream changes can be updated with::

  git submodule update --remote

Distribution packages to PyPI can be created with::

  python setup.py sdist
  python setup.py bdist_wheel

Distribution packages can be uploaded to PyPI with::

  twine upload dist/wundertool-[version].tar.gz
  twine upload dist/wundertool-[version]-py3-none-any.whl
