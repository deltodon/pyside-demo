PySide Demo Documentation
=========================

Welcome to the PySide Demo documentation. This project demonstrates an offline-first GUI application with PostgreSQL synchronization using PySide6.

.. image:: images/pyside-demo-anim.gif
   :width: 700
   :alt: PySide Demo Animation

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   data
   modules/index
   contributing
   changelog
   troubleshooting

Introduction
------------

PySide Demo is a Python application that showcases how to build a robust, offline-first GUI application using PySide6 with PostgreSQL synchronization capabilities.

Quick Start
-----------

To get started with PySide Demo, follow these steps:

1. Clone the repository

   .. code-block:: bash

      git clone https://github.com/deltodon/pyside-demo.git

      cd pyside-demo

2. Install the project using Poetry:

   .. code-block:: bash

      poetry install

3. Run the application:

   .. code-block:: bash

      poetry run python -m pyside_demo

For more detailed instructions, see the :doc:`installation` and :doc:`usage` pages.

Features
--------

- Offline-first architecture
- Local data storage in SQLite
- PySide6 based GUI
- PostgreSQL synchronization
- Interactive Graph visualisation
- Interactive Geospatial data visualisation
- Custom QSS colour theme
- Cross-platform support
- Model View Controller structure (MVC)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
