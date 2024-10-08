# Contributing

We welcome contributions to the PySide Demo project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/your-username/pyside-demo.git
   cd pyside-demo
   ```

3. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature-or-fix-name
   ```

4. Make your changes and commit them with a clear commit message.
5. Push your changes to your fork:

   ```bash
   git push --set-upstream origin feature-or-fix-name
   ```

6. Open a pull request on the original repository.

## Coding Standards

* Follow PEP 8 style guide for Python code.
* Use type hints where appropriate.
* Write clear, concise comments and docstrings.
* Ensure your code is compatible with Python 3.9+.

## Development

* Open Qt Designer

   ```bash
   poetry run pyside6-designer
   ```

* Search for qtawesome icons

   ```bash
   poetry run qta-browser
   ```

* Build the project:

   ```bash
   poetry run pyside6-project build pyside_demo
   ```

## Testing

* Add unit tests for new functionality.
* Ensure all tests pass before submitting a pull request.

* Run tests using pytest:

  ```bash
  poetry run python -m pytest -v
  ```

* Run mypy test:

   ```bash
   poetry run mypy pyside_demo
   ```

* or run mypy test with pre-commit:

   ```bash
   poetry run pre-commit run mypy --all-files
   ```

* Run all lint tests

   ```bash
   poetry run pre-commit run --all-files
   ```

## Documentation

* Update documentation for any new features or changes in behavior.
* Use clear, concise language in your documentation.

## Submitting Pull Requests

* Provide a clear description of the problem and solution.
* Include any relevant issue numbers.
* Ensure CI checks pass on your pull request.

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

Thank you for contributing to PySide Demo!
