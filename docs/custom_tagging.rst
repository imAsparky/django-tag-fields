Customizing tag-fields
======================

Using a Custom Tag or Through Model
-----------------------------------
The tool ``django-tag-fields`` uses a ``through model`` with a
``GenericForeignKey`` and another ``ForeignKey`` to an included ``Tag`` model.

However, this may not be ideal in certain situations, such as needing the speed
and referential guarantees of a real ``ForeignKey,`` having a model with a
non-integer primary key or wanting to store extra data about a tag.
Fortunately, ``django-tag-fields`` allows you to easily substitute your own
through model or Tag model to address these issues.

Note that if you include ``tag-fields`` in the ``settings.py`` INSTALLED_APPS
list, the default ``django-tag-fields`` and ``through model`` models will be
created.

If you prefer custom models, remove ``tag_fields`` from the INSTALLED_APPS list
in ``settings.py.``

To change the behaviour, you can subclass several classes to achieve different
outcomes.

==================================    ====================================================================================================
Class name                            Behavior
==================================    ====================================================================================================
``ThroughTableBase``                  Abstract Base Class: ``through table`` for all ``through table`` subclasses.
``TaggedItemThroughBase``             Abstract Base Class: ``through table`` for a ``Tagged Item`` model.
``GenericFKTaggedItemThroughBase``    Abstract Base Class: ``through table`` for a ``Tagged Item`` model using an ``GenericForeignKey``.
``IntegerFKTaggedItemThroughBase``    Abstract Base Class: ``through table`` for a ``Tagged Item`` model using an ``integer`` primary key.
``UUIDFKTaggedItemThroughBase``       Abstract Base Class: ``through table`` for a ``Tagged Item`` model using an ``UUID`` primary key.
==================================    ====================================================================================================

Custom ForeignKeys
~~~~~~~~~~~~~~~~~~

Your intermediary model must be a subclass of
``tag_fields.models.TaggedItemThroughBase`` with a foreign key to your content
model named ``content_object``.

Pass this intermediary model as the ``through`` argument to ``TaggableManager``:

  .. code-block:: python

    from django.db import models

    from tag_fields.managers import TaggableManager
    from tag_fields.models import TaggedItemThroughBase


    class TaggedFood(TaggedItemThroughBase):
        content_object = models.ForeignKey('Food', on_delete=models.CASCADE)

    class Food(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedFood)


Once this is done, the API works the same as for GFK-tagged models.

Custom GenericForeignKeys
~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``GenericForeignKey`` used by ``django-tag-fields`` assume your
tagged object uses an integer primary key. For non-integer primary key,
your intermediary model must be a subclass of ``tag_fields.models.GenericFKTaggedItemThroughBase``
with a field named ``object_id`` of the type of your primary key.

For example, if your primary key is a string:

  .. code-block:: python

    from django.db import models

    from tag_fields.managers import TaggableManager
    from tag_fields.models import (
                                   GenericFKTaggedItemThroughBase,
                                   TaggedItemThroughBase,
                                  )

    class GenericStringTaggedItem(GenericFKTaggedItemThroughBase, TaggedItemThroughBase):
        object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)

    class Food(models.Model):
        food_id = models.CharField(primary_key=True)
        # ... fields here

        tags = TaggableManager(through=GenericStringTaggedItem)

UUIDFKTaggedItemThroughBase
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A common use case of a non-integer primary key is the UUID primary key.
``django-tag-fields`` provides a base class ``UUIDFKTaggedItemThroughBase`` ready
to use with models using a UUID primary key:

  .. code-block:: python

    from django.db import models
    from django.utils.translation import gettext_lazy as _

    from tag_fields.managers import TaggableManager
    from tag_fields.models import (
                                   UUIDFKTaggedItemThroughBase,
                                   TaggedItemThroughBase,
                                  )

    class UUIDTaggedItem(UUIDFKTaggedItemThroughBase, TaggedItemThroughBase):
        # If you only inherit UUIDFKTaggedItemThroughBase, you need to define
        # a tag field. e.g.
        # tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

        class Meta:
            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

    class Food(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        # ... fields here

        tags = TaggableManager(through=UUIDTaggedItem)

Custom tag
~~~~~~~~~~

When providing a custom ``Tag`` model, it should be a ``ForeignKey`` to your
tag model named ``"tag"``. If your custom ``Tag`` model has extra parameters
you want to initialize during setup, you can pass it along via the
``tag_kwargs`` parameter of ``TaggableManager.add``.

For example, ``my_food.tags.add("tag_name1", "tag_name2", tag_kwargs={"my_field":3})``:

.. code-block:: python

    from django.db import models
    from django.utils.translation import gettext_lazy as _

    from tag_fields.managers import TaggableManager
    from tag_fields.models import TagBase, GenericFKTaggedItemThroughBase


    class MyCustomTag(TagBase):
        # ... fields here

        class Meta:
            verbose_name = _("Tag")
            verbose_name_plural = _("Tags")

        # ... methods (if any) here


    class TaggedWhatever(GenericFKTaggedItemThroughBase):
        # TaggedWhatever can also extend TaggedItemThroughBase or a combination
        # of both TaggedItemThroughBase and GenericFKTaggedItemThroughBase.
        # GenericFKTaggedItemThroughBase allows using the same tag for
        # different kinds of objects, in this example Food and Drink.

        # Here is where you provide your custom Tag class.
        tag = models.ForeignKey(
            MyCustomTag,
            on_delete=models.CASCADE,
            related_name="%(app_label)s_%(class)s_items",
        )


    class Food(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedWhatever)


    class Drink(models.Model):
        # ... fields here

        tags = TaggableManager(through=TaggedWhatever)


.. class:: TagBase

    .. method:: slugify(tag, i=None)

      The ``tag-fields`` feature uses the :func:`django.utils.text.slugify`
      as the default method to generate a slug for a tag.

      But if you wish to use your logic, you can customize this process by
      overriding the method.

      The method takes in two arguments: the ``tag`` as a string and an
      ``integer`` ``i``. If ``i`` is ``None``, it's the first attempt to
      generate a slug for the tag, while a number greater than zero indicates
      the number of attempts to create a unique slug.


Using a custom tag string parser
--------------------------------

By default, ``django-tag-fields`` uses ``tag_fields.utils._parse_tags``, which
accepts a string that may contain one or more tags and returns a list of tag
names.

This parser is quite intelligent and can handle many edge cases; however, you
may wish to provide your parser for various reasons e.g.

* you can do some preprocessing on the tags so that they are converted to
  lowercase
* reject certain tags
* disallow certain characters
* split only on commas rather than commas and whitespace
* etc

To provide your parser, write a function that takes a tag string and returns
a list of tag names.


For example, see a simple function to split on comma's and convert to lowercase
below.

  .. code-block:: python

    def comma_splitter(tag_string):
        return [t.strip().lower() for t in tag_string.split(',') if t.strip()]


To use a specific function instead of the string parser, add a new setting
called "TAGS_GET_TAGS_FROM_STRING" and provide its dotted path to your desired
function.


You can also offer a function that transforms a collection of tags into a
string format. To change the default value
(which is "tag_fields.utils._edit_string_for_tags"), use the
"TAGS_GET_STRING_FROM_TAGS" setting.

  .. code-block:: python

    def comma_joiner(tags):
        return ', '.join(t.name for t in tags)

To define the above functions in a module called "appname.utils", your
project's settings.py file should include the following.

  .. code-block:: python

    TAGS_GET_TAGS_FROM_STRING = 'appname.utils.comma_splitter'
    TAGS_GET_STRING_FROM_TAGS = 'appname.utils.comma_joiner'
