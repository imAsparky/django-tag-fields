Usage With Django Rest Framework
================================

Because the tags in ``django-tag-fields`` need to be added into a ``TaggableManager()``
we cannot use the usual ``Serializer`` that we get from Django REST Framework.
Because this is trying to save the tags into a ``list``, which will throw an exception.

To accept tags through a `REST` API call we need to add the following to our ``Serializer``.


.. code-block:: python

    from tag_fields.serializers import (
                                        TagListSerializerField,
                                        TaggitSerializer,
                                        )


    class YourSerializer(
                          TaggitSerializer,
                          serializers.ModelSerializer,
                        ):

        class Meta:
            model = YourModel
            fields = '__all__'

        tags = TagListSerializerField()



And you're done, so now you can add tags to your model.
