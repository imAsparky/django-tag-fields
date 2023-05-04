Usage With Django Rest Framework
================================

To add tags into a ``TaggableManager()`` using ``django-tag-fields``, the usual
``Serializer`` from Django REST Framework cannot be used.

Attempting to save the tags into a list using ``DRF Serializer`` will cause
an exception.

To enable the acceptance of tags via a REST API call, you need to add the
following to the ``Serializer``.


.. code-block:: python

    from tag_fields.serializers import (
        TagSerializer,
        TagListSerializerField,
    )



    class YourSerializer(
        TagSerializer,
        serializers.ModelSerializer,
    ):

        class Meta:
            model = YourModel
            fields = '__all__'

        tags = TagListSerializerField()



You can now add tags to your model via a REST API call.
