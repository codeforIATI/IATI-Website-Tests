IATI Status
===========

Monitoring the status of live IATI services and websites.

The current overall status is shown on the badge below:

.. image:: https://raw.githubusercontent.com/codeforIATI/iati-status/gh-pages/status.svg
    :target: https://iati-status.codeforiati.org/

Tests are run daily using Github Actions. Pytest outputs a report.json file, which is pushed to the ``gh-pages`` branch.

Setup
-----

.. code-block:: bash

	# Create a virtual environment using python 3
	python3 -m venv venv

	# Activate the virtual environment
	source venv/bin/activate

	# Install requirements
	pip install -r requirements.txt

	# Run the tests
	pytest
