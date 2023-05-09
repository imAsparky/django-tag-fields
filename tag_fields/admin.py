from django.contrib import admin

from tag_fields.models import ModelTag, ModelTagIntFk


class TaggedItemInline(admin.StackedInline):
    model = ModelTagIntFk


@admin.register(ModelTag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
