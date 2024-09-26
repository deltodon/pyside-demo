# PySide Demo

|   |   |
|---|---|
|Project|[![Python Versions](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/) [![Supported Platforms](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](https://github.com/deltodon/pyside-demo) [![License](https://img.shields.io/github/license/deltodon/pyside-demo)](LICENSE) |
|Quality| [![Issues](https://img.shields.io/github/issues/deltodon/pyside-demo)](https://github.com/deltodon/pyside-demo/issues) [![Lint](https://img.shields.io/badge/Lint-black%20%7C%20isort%20%7C%20flake8%20%7C%20mypy%20%7C%20pymarkdown-blue)](https://github.com/deltodon/pyside-demo/blob/main/.pre-commit-config.yaml) |
| Tools | [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/) |

This application is a PySide6-based GUI that demonstrates an offline-first approach with PostgreSQL synchronization capabilities.
It allows users to manage items locally and synchronize them with a remote PostgreSQL database when an internet connection is available.

It uses folium and pyqtgraph for interactive graph and geospatial visualisation.

![PySide Demo Animation](https://github.com/deltodon/pyside-demo/blob/main/docs/images/pyside-demo-anim.gif)

* [Introduction](https://deltodon.github.io/pyside-demo/introduction.html)
* [Installation](https://deltodon.github.io/pyside-demo/installation.html)
* [Usage](https://deltodon.github.io/pyside-demo/usage.html)
* [Data](https://deltodon.github.io/pyside-demo/data.html)
* [Contributing](https://deltodon.github.io/pyside-demo/contributing.html)
* [Changelog](https://deltodon.github.io/pyside-demo/changelog.html)

### Quick Start

install the package using pip

```bash
pip install pyside-demo
```

run the package

```bash
python -m pyside_demo
```

if you are using Poetry, install the package  with

```bash
poetry add pyside-demo
```

and then run

```bash
poetry run python pyside_demo
```

### Features

* Offline-first architecture
* Local data storage in SQLite
* PySide6 based GUI
* PostgreSQL synchronization
* Interactive Graph visualisation
* Interactive Geospatial data visualisation
* Custom QSS colour theme
* Cross-platform support
* Model View Controller structure (MVC)
