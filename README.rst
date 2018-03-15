=========================
Core Oaipmh Harvester App
=========================

OAI-PMH harvesting capabilities for the curator core project.

Quickstart
==========

1. Add "core_oaipmh_harvester_app" to your INSTALLED_APPS setting
-----------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_oaipmh_harvester_app',
    ]

2. Include the core_oaipmh_harvester_app URLconf in your project urls.py
------------------------------------------------------------------------

.. code:: python

    url(r'^oai_pmh/', include('core_oaipmh_harvester_app.urls')),
