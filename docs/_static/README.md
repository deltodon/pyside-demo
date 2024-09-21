# _static

The `_static` directory is designed to hold static files intended to be included in the documentation. These files can be:

* **Custom CSS and JavaScript files:** To modify or extend the styling and interactivity of the documentation beyond the default theme.

* **Images and media assets:** That are referenced in your documentation but are not part of the source `.rst` files.

* **Fonts and other assets:** Any other static resources that need to be accessible in your built documentation.

### Usage

#### Including Custom CSS

* Place your `custom.css` file inside the `_static` directory.

* In your `conf.py`, add the following lines:

    ```python
    html_static_path = ['_static']
    html_css_files = ['custom.css']
    ```

#### Referencing Static Files in Documentation

* Use reStructuredText directives to include images or other media:

    ```rst
    .. image:: /_static/my_image.png
       :alt: My Image
    ```

### Behavior During Build

* When you build your documentation (e.g., with `make html`), Sphinx copies the contents of the `_static` directory to the output directory (e.g., `_build/html/_static/`).

* All paths referencing `_static` in your documentation will correctly link to these files in the built HTML.
