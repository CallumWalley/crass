import sys
import os


project = 'crass'
copyright = '2024, cal'
author = 'cal'
release = '0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
extensions = [
   'sphinx.ext.duration',
   'sphinx.ext.doctest',
   'sphinx.ext.autodoc',
   'sphinx.ext.autosummary',
]
sys.path.append(os.path.abspath('sphinxext'))
