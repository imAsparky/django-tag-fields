from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models, router, transaction
from django.utils.text import slugify
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

try:
    from unidecode import unidecode
except ImportError:

    def unidecode(tag):
        return tag


class TagBase(models.Model):
    """Abstract Base class for the tags."""

    class Meta:
        abstract = True

    name = models.CharField(
        verbose_name=pgettext_lazy("A tag name", "name"),
        unique=True,
        max_length=100,
    )
    slug = models.SlugField(
        verbose_name=pgettext_lazy("A tag slug", "slug"),
        unique=True,
        max_length=100,
        allow_unicode=True,
    )

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = self.slugify(self.name)
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self
            )
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be opportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with transaction.atomic(using=using):
                    res = super().save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(
                type(self)
                ._default_manager.filter(slug__startswith=self.slug)
                .values_list("slug", flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrency issues here for now.
                    # (That is, till we found a nice solution...)
                    return super().save(*args, **kwargs)
                i += 1
        else:
            return super().save(*args, **kwargs)

    def slugify(self, tag, i=None):
        if getattr(settings, "TAGS_STRIP_UNICODE_WHEN_SLUGIFYING", False):
            slug = slugify(unidecode(tag))
        else:
            slug = slugify(tag, allow_unicode=True)
        if i is not None:
            slug += "_%d" % i
        return slug


class Tag(TagBase):
    """Model tag for use with your own model.

    This is a model level tag, i.e. there can only be one per model.

    """

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")
        app_label = "tag_fields"


class ThroughTableBase(models.Model):
    """Base class for a model ``tags`` through table.

    Abstract Base Class: ``through table`` for all ``through table``
    sub classes.

    taggit class name was ItemBase

    """

    class Meta:
        abstract = True

    def __str__(self):
        return gettext("%(object)s tagged with %(tag)s") % {
            "object": self.content_object,
            "tag": self.tag,
        }

    @classmethod
    def tag_model(cls):
        field = cls._meta.get_field("tag")
        return field.remote_field.model

    @classmethod
    def tag_relname(cls):
        field = cls._meta.get_field("tag")
        return field.remote_field.related_name

    @classmethod
    def lookup_kwargs(cls, instance):
        return {"content_object": instance}

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        kwargs = extra_filters or {}
        if instance is not None:
            kwargs.update({"%s__content_object" % cls.tag_relname(): instance})
            return cls.tag_model().objects.filter(**kwargs)
        kwargs.update(
            {"%s__content_object__isnull" % cls.tag_relname(): False}
        )
        return cls.tag_model().objects.filter(**kwargs).distinct()


class TaggedItemThroughBase(ThroughTableBase):
    """Sub class of ``ThroughTableBase``

    Base class: ``through table`` for a ``Tagged Item`` model.

    taggit class name was TaggedItemBase

    """

    class Meta:
        abstract = True

    tag = models.ForeignKey(
        Tag,
        related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE,
    )


class GenericFKTaggedItemThroughBase(ThroughTableBase):
    """Abstract subclass of ``ThroughTableBase`` using a ``GenericForeignKey``.

    Base class: ``through table`` for a ``Tagged Item`` model using an
    ``GenericForeignKey``.

    taggit class name was CommonGenericTaggedItemBase


    """

    class Meta:
        abstract = True

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("content type"),
        related_name="%(app_label)s_%(class)s_tagged_items",
    )
    content_object = GenericForeignKey()

    @classmethod
    def lookup_kwargs(cls, instance):
        return {
            "object_id": instance.pk,
            "content_type": ContentType.objects.get_for_model(instance),
        }

    @classmethod
    def tags_for(cls, model, instance=None, **extra_filters):
        tag_relname = cls.tag_relname()
        model = model._meta.concrete_model
        kwargs = {
            "%s__content_type__app_label" % tag_relname: model._meta.app_label,
            "%s__content_type__model" % tag_relname: model._meta.model_name,
        }
        if instance is not None:
            kwargs["%s__object_id" % tag_relname] = instance.pk
        if extra_filters:
            kwargs.update(extra_filters)
        return cls.tag_model().objects.filter(**kwargs).distinct()


class IntegerFKTaggedItemThroughBase(GenericFKTaggedItemThroughBase):
    """Abstract subclass of ``GenericFKTaggedItemThroughBase`` with
     ``Integer Foreign Key``.

    Base class: ``through table`` for a ``Tagged Item`` model using an
    ``integer`` primary key.

    taggit class name was GenericTaggedItemBase

    """

    class Meta:
        abstract = True

    object_id = models.IntegerField(verbose_name=_("object ID"), db_index=True)


class UUIDFKTaggedItemThroughBase(GenericFKTaggedItemThroughBase):
    """Abstract subclass of CommonGenericTaggedItemBase with a
      ```UUID Foreign Key``.

    Base class: ``through table`` for a ``Tagged Item`` model using an ``UUID``
    primary key.

    taggit class name was GenericUUIDTaggedItemBase

    """

    class Meta:
        abstract = True

    object_id = models.UUIDField(verbose_name=_("object ID"), db_index=True)


class TaggedItem(IntegerFKTaggedItemThroughBase, TaggedItemThroughBase):
    """Tagged Item Through Table using Integer Foreign Key.

    Allows custom Tag models. Tagged models use a ``Integer`` primary key.

    taggit class name was TaggedItem

    .. note::

        Changing this class name breaks the tests. Some checks made to see what
        was causing the error but it requires more time.

    """

    class Meta:
        verbose_name = _("tagged item")
        verbose_name_plural = _("tagged items")
        app_label = "tag_fields"
        index_together = [["content_type", "object_id"]]
        unique_together = [["content_type", "object_id", "tag"]]
