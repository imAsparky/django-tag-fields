extensions = ["sphinx.ext.intersphinx"]

master_doc = "index"

project = "django-tag-fields"
copyright = "Alex Gaynor, Mark Sevelj and individual contributors."

__version__ = "4.0.2"
# The full version, including alpha/beta/rc tags.
release = __version__

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
}
