ssacc - Map SSA County Codes and ZIP codes (ZIP-5)
==================================================

.. image:: https://github.com/tomwillis608/ssacc/workflows/CI/badge.svg
    :target: https://github.com/tomwillis608/ssacc/actions?workflow=CI
    :alt: GitHub Actions CI Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: black

.. image:: https://sonarcloud.io/api/project_badges/measure?project=tomwillis608_ssacc&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=tomwillis608_ssacc
    :alt: sonarcloud

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit
    :alt: pre-commit

.. image:: https://codecov.io/gh/tomwillis608/ssacc/branch/main/graph/badge.svg?token=P714209P32
    :target: https://codecov.io/gh/tomwillis608/ssacc
    :alt: CodeCov

.. image:: https://www.codefactor.io/repository/github/tomwillis608/ssacc/badge?style=plastic
    :target: https://www.codefactor.io/repository/github/tomwillis608/ssacc
    :alt: CodeFactor reviews

.. image:: https://snyk.io/test/github/tomwillis608/ssacc/badge.svg
    :target: https://snyk.io/test/github/tomwillis608/ssacc/
    :alt: Snyk Tests

.. image:: https://api.codeclimate.com/v1/badges/97ee5c5cbbbb16c9fc4a/maintainability
   :target: https://codeclimate.com/github/tomwillis608/ssacc/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/97ee5c5cbbbb16c9fc4a/test_coverage
   :target: https://codeclimate.com/github/tomwillis608/ssacc/test_coverage
   :alt: Test Coverage

.. image:: https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg
   :target: https://houndci.com
   :alt: Reviewed by Hound

Sloppy Python project that can grab source tables from the internet, extract relationships between
SSA Country Codes and ZIPs through intermediary relationship to FIPS county codes.

SSA County Codes are used in some CMS databases, like NCH Part A, rather than FIPS county codes. This is an
attempt to create tables that show a mapping of USPS ZIP-5 Codes to SSA County Codes, along with other location
information associated with ZIP Codes.

TODO: project-ify it for pip.

Before running the Python, you need to download some input files from the internet.
Run the ``fetch_batch.bat`` file if running from Windows.
If running from \*nix, you will need to curl the three files by hand and unzip the one.

The first time you run the ``python -m ssacc.cli``, run with the ``-r 1`` option to generate
``data/source/zipcodes.csv`` intermediate file. The goal is to create
``data/ssa_cnty_zip.csv`` which maps ZIP-5 to SSA Country Code, including the
3-digit county-only value and the 5-digit value that includes the state code.
If you want to iterate over the data without regenerating ``data/sources/zipcodes.csv``
run with the ``-r 0`` or no ``-r`` command line argument.

The column headers are:

- zip - 5-digit ZIP code
- ssacnty - SSA 3-digit country code
- ssastco - SSA 5-digit county code, with 2-digit state code prepended
- countyname - Text name of the county, title case
- city - Text name of city, title case
- stabbr - Postal 2-character state code
- state - Text name of state, title case

Requirements
------------

Python 3.6+.


Windows Support
---------------

Developed on Windows 10, initially (Note the batch file). More recently with WSL.

Dependencies
------------

Dependencies are defined in:

- ``requirements.in``

- ``requirements.txt``

- ``dev-requirements.in``

- ``dev-requirements.txt``

Virtual Environments
^^^^^^^^^^^^^^^^^^^^

It is best practice during development to create an isolated
`Python virtual environment <https://docs.python.org/3/library/venv.html>`_ using the
``venv`` standard library module. This will keep dependant Python packages from interfering
with other Python projects on your system. I let PyCharm magically take care of this.

To setup the virtual environment locally, as in the ``travis.yml``:

.. code-block:: console

    (venv) $ pip install --upgrade virtualenv

    (venv) $ pip install tox

    (venv) $ pip install codecov

    (venv) $ pip install pytest

python3 -m venv env

source env/bin/activate
Testing
-------

Automated testing is performed using `tox <https://tox.readthedocs.io/en/latest/index.html>`_.
tox will automatically create virtual environments based on ``tox.ini`` for unit testing,
PEP8 style guide checking, and documentation generation.

To run all the tests:

.. code-block:: console

    (venv) $ tox

Unit Testing
^^^^^^^^^^^^

To Do: Add meaningful unit tests and refactor into more testable code.

Unit testing is performed with `pytest <https://pytest.org/>`_. pytest has become the de facto
Python unit testing framework.

pytest will automatically discover and run tests by recursively searching for folders and ``.py``
files prefixed with ``test`` for any functions prefixed by ``test``.

The ``tests`` folder is created as a Python package (i.e. there is an ``__init__.py`` file
within it) because this helps ``pytest`` uniquely namespace the test files. Without this,
two test files cannot be named the same, even if they are in different sub-directories.

Code coverage is provided by the `pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`_
plugin.

Code coverage is configured in ``pyproject.toml``.


Automated Code Formatting
^^^^^^^^^^^^^^^^^^^^^^^^^

Code is automatically formatted using `black <https://github.com/psf/black>`_. Imports are
automatically sorted and grouped using `isort <https://github.com/timothycrosley/isort/>`_.

These tools are configured by:

- ``pyproject.toml``

To automatically format code, run:

.. code-block:: console

    (venv) $ tox -e fmt

To verify code has been formatted, such as in a CI job:

.. code-block:: console

    (venv) $ tox -e fmt-check

Project Structure
-----------------

The project directory structure is like:

.. code-block::

    ssacnt
    ├── ssacnt
    │   ├── __init__.py
    │   ├── cli.py
    │   └── <lib>.py
    ├── tests
    │   ├── __init__.py
    |   |── unit
    │       ├── __init__.py
    │       └── test_<lib>.py
    │── data
    │   ├── ssa_cnty_zip.csv <<-- This is the final output generated
    │   └── <ephemeral folders>
    ├── tox.ini
    └── setup.py

Licensing
---------

Licensing for the project is defined in:

- ``LICENSE.txt``

- ``setup.py``

This project uses a common permissive license, the MIT license.

Thanks to Brian Gruber for the head start from https://github.com/bgruber/zip2fips, from
which I shamelessly borrowed.
