Frequently Asked Questions
==========================

1. How can I get all my tags?
-----------------------------

To start using tags, you can access the pre-built ``Tag`` model
in ``tag_fields.models``.

However, if you have a custom model derived
from ``ThroughTableBase``you will need to query that instead.

For the standard setup, use ``Tag.objects.all()`` to retrieve all the
available tags.



2. How can I use this with factory_boy?
---------------------------------------

To handle tags, refer to `factory_boy's documentation on many-to-many
relationships <https://factoryboy.readthedocs.io/en/stable/recipes.html
#simple-many-to-many-relationship>`_ for insights and ideas.


One way to handle this is with post-generation hooks.

.. code-block:: python

    class ProductFactory(DjangoModelFactory):
        # Rest of the stuff

        @post_generation
        def tags(self, create, extracted, **kwargs):
            if not create:
                return

            if extracted:
                self.tags.add(*extracted)
