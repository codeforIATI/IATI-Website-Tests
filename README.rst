IATI Website Tests
==================

.. image:: https://travis-ci.com/codeforIATI/IATI-Website-Tests.svg?branch=master
    :target: https://travis-ci.com/codeforIATI/IATI-Website-Tests
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/codeforIATI/IATI-Website-Tests/blob/master/LICENSE


Introduction
------------

This repository contains smoke tests and sanity checks for all live IATI websites and web tools.

The output of tests can be seen at: https://travis-ci.com/codeforIATI/IATI-Website-Tests


Technology Overview
-------------------

Tests are written using `pytest <http://doc.pytest.org>`_ using Python 3.7.

Most tests are designed to obtain HTML and associated content from IATI websites, using the `requests library <http://docs.python-requests.org>`_. This retries failed requests several times should a failure occur, so as to reduce flakiness. Additional tests on the status of backups are made using the `paramiko module <http://www.paramiko.org>`_, which checks the status of expected backup files via an SSH connection.

These tests are run daily using Travis `cron jobs <https://docs.travis-ci.com/user/cron-jobs/>`_.

For a more detailed of the test architecture, view the README under `tests`.

The current status of the tests can be seen `on the Travis site <https://travis-ci.com/codeforIATI/IATI-Website-Tests>`_. 


Installation
------------

.. code-block:: bash

	# Create a virtual environment using python 3
	python3 -m venv pyenv

	# Activate the virtual environment
	source pyenv/bin/activate

	# Install requirements
	pip install -r requirements.txt

	# Login credentials for the IATI backup server are stored as environment variables.
	# Add these lines to the end of your virtualenv set-up script - i.e. pyenv/bin/activate
	export backup_server_hostname='[YOUR_HOSTNAME]'
	export backup_server_username='[YOUR_USERNAME]'
	export backup_server_password='[YOUR_PASSWORD]'

	# Run the tests
	py.test tests/
