# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path('..', 'src').resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'WarEraAPI'
copyright = '2026, SpicyPenguin'
author = 'SpicyPenguin'
release = '0.2.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.apidoc"]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = []

apidoc_modules = [
    {
        'path': '../../src/WarEraAPI',
        'destination': 'apidocs/',
        'exclude_patterns': ['**/test*', '**/__pycache__*'],
        'max_depth': 4,
        'follow_links': True,
        'separate_modules': True,
        'include_private': False,
        'no_headings': False,
        'module_first': True,
        'implicit_namespaces': False,
        'automodule_options': {
            'members', 'show-inheritance', 'undoc-members'
        },
    },
]
