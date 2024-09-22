# Installation

This guide will help you set up PySide Demo on your local machine.

## Prerequisites

* Python 3.9 or higher
* Poetry (for dependency management)
* PostgreSQL server (for remote synchronization)

## Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pyside-demo.git
   cd pyside-demo
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Install pre-commit hooks (optional):

   ```bash
   poetry run pre-commit install
   ```

4. Run the application:

   ```bash
   poetry run python -m pyside_demo
   ```

## Configuration

Before running the application, you need to configure the PostgreSQL connection details:

1. Open `gui.py`
2. Locate the `sync_with_postgresql` method in the `MainWindow` class
3. Update the following variables with your PostgreSQL server details:

```python
host = "your_host"
database = "your_database"
user = "your_username"
password = "your_password"
```

## Troubleshooting

If you encounter any issues during installation, please check the following:

* Ensure you have the correct Python version installed
* Make sure Poetry is installed and up to date
* Check that all required system libraries are installed (e.g., Qt dependencies)

For more detailed troubleshooting, please refer to the project's GitHub issues or contact the maintainers.
