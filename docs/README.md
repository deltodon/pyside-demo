# Documentation

* [Introduction](introduction.md)
* [Installation](installation.md)
* [Usage](usage.md)
* [Contributing](contributing.md)
* [Changelog](changelog.md)

### Build Sphinx

1. navigate to docs directory

    ```bash
    cd docs
    ```

2. delete old build

    ```bash
    poetry run make clean
    ```

3. create new build

    ```bash
    poetry run make html
    ```

### Notes

The follwing warning

```bash
docs/docstring of pyside_demo.db.database.Base.metadata:6: WARNING: undefined label: 'orm_declarative_metadata'
```

caused by [Sphinx shows warnings for a code that imports latest version of SQLAlchemy==2.0.4 #11212](https://github.com/sphinx-doc/sphinx/issues/11212)
