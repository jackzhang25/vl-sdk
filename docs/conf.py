# Configuration file for the Sphinx documentation builder.
import os
import sys

# Add the package source to Python path for autodoc
sys.path.insert(0, os.path.abspath('../src'))

# Import version from package
try:
    from visual_layer_sdk import __version__
    release = __version__
except ImportError:
    # Fallback version if package can't be imported
    release = '0.1.5'

# -- Project information -----------------------------------------------------
project = 'Visual Layer SDK'
copyright = '2024, Jack Zhang'
author = 'Jack Zhang'
version = release

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx_copybutton',
]

# Support both .md and .rst files
source_suffix = ['.rst', '.md']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_title = 'Visual Layer SDK'

html_theme_options = {
    "sidebar_hide_name": False,
    "light_logo": "logo-light.svg",
    "dark_logo": "logo-dark.svg",
    "light_css_variables": {
        "color-brand-primary": "#267CB9",
        "color-brand-content": "#267CB9",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4A9EDA",
        "color-brand-content": "#4A9EDA",
    },
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/jackzhang25/vl-package",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_static_path = ['_static']

# MyST Parser configuration for Markdown support
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Copy button configuration
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True