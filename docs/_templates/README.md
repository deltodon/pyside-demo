# _templates

The `_templates` directory is used to store custom HTML templates that override or extend the default templates provided by Sphinx or the theme.

### Usage

* **Customizing Layouts:**
  * Create an `index.html` or `layout.html` in `_templates` to modify the structure of your pages.

* **Adding Custom Elements:**
  * Insert analytics scripts, custom headers, footers, or modify sidebars.
  
* **Extending Base Templates:**
  * Use Jinja2 templating language to extend and override parts of the base templates.

### Configuration

* Ensure your `conf.py` includes the `_templates` path:

  ```python
  templates_path = ['_templates']
  ```

* Example of extending a template:

  ```html
  <!-- _templates/layout.html -->
  {% extends "!layout.html" %}

  {% block extrahead %}
    {{ super() }}
    <link rel="stylesheet" href="{{ pathto('_static/custom.css', 1) }}">
  {% endblock %}
  ```

### Behavior During Build

* Sphinx uses these templates during the build process to generate the HTML files.

* Custom templates override the default ones if they have the same name.
