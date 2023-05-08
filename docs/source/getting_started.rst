Getting Started
===============

To get started using ``django-tag-fields`` simply install it with
``pip``.

.. code-block:: console

    $ pip install django-tag-fields


Add ``"tag_fields"`` to your project's ``INSTALLED_APPS`` setting and ``migrate``.

.. code-block:: console

    ./manage.py migrate


And then, to any model you want tagged, do the following.

.. code-block:: python

    from django.db import models

    from tag_fields.managers import TaggableManager

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager()


.. tip::

    To make ``django-tag-fields`` search for existing tags in a
    case-insensitive way, you need to modify the ``TAGS_CASE_INSENSITIVE``
    setting.

    By default, it is set to ``False``, but you can change it to ``True`` in
    your Django settings file or wherever you store your settings.

    .. code-block:: python

      TAGS_CASE_INSENSITIVE = True


Settings
--------

You can alter ``django-tag-fields`` behaviour by changing the Django-level
settings below.

.. code-block:: python


  TAGS_CASE_INSENSITIVE

  """"
  Defaults to ``False``.  When set to ``True``, tag lookups will be case
  insensitive.
  """

.. code-block:: python

  TAGS_STRIP_UNICODE_WHEN_SLUGIFYING

  """"
  Defaults to False.  When set to True, tag slugs will be limited to ASCII
  characters.

  If ``True`` and you also have ``unidecode`` installed,
  then tag sluggification will transform a tag like (あい うえお) to (ai-ueo).

  If ``True`` and do not have ``unidecode`` installed, then you will usually
  be stripping Unicode, meaning that something like ``helloあい`` will be
  slugified as ``hello``.
  """

.. caution::

  The behaviour of ``TAGS_STRIP_UNICODE_WHEN_SLUGIFYING`` , when ``True``,
  leads to situations where  slugs can be entirely stripped to an empty string;
  we **dont** recommend activating this.
