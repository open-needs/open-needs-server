# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Open-Needs Server'
copyright = '2022, Open-Needs community'
author = 'Open-Needs community'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autosummary",
    "sphinx_immaterial",
    'sphinxcontrib.autodoc_pydantic'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_immaterial'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

############


# material theme options (see theme.conf for more information)
html_theme_options = {
    # "icon": {
    #     "repo": "open-needs/open-needs-server",
    # },
    "site_url": "https://open-needs.org/open-needs-server",
    "repo_url": "https://github.com/open-needs/open-needs-server",
    "repo_name": "Open-Needs Server",
    "repo_type": "github",
    "edit_uri": "blob/main/docs",
    # "google_analytics": ["UA-XXXXX", "auto"],
    "globaltoc_collapse": True,
    "features": [
        # "navigation.expand",
        # "navigation.tabs",
        # "toc.integrate",
        "navigation.sections",
        # "navigation.instant",
        # "header.autohide",
        "navigation.top",
        # "navigation.tracking",
        # "search.highlight",
        "search.share",
    ],
    "palette": [
        {
            # "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "white",
            "accent": "indigo",
        }

    ],
    "version_dropdown": False,
    # "version_info": [
    #     {
    #         "version": "https://open-needs/server",
    #         "title": "open-Needs",
    #         "aliases": []
    #     },
    # ],
    "toc_title_is_page_title": True,
}  # end html_theme_options

html_last_updated_fmt = ""
html_use_index = False
html_domain_indices = False
