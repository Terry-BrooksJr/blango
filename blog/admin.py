"""
Module Docstring: blog.admin

This module contains the admin definitions for the blog app, including the PostAdmin and TagAdmin classes.

The PostAdmin class defines the admin interface for the Post model, allowing for the management and display of post data in the Django admin interface. 
It includes custom admin actions for marking selected posts as published.

The TagAdmin class defines the admin interface for the Tag model, but currently does not include any custom admin actions.

To use these admin definitions, they must be registered with the Django admin site using the admin.site.register() method.

"""

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import ngettext

from blog.models import Post, Tag, Comment


# SECTION - Admin Models Defintions
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'created_at'
    list_display = ['title', 'author', 'created_at', 'slug', 'published_at']
    actions = ['make_published']

    # SECTION - Custom Admin Actions
    @admin.action(description='Mark selected posts as published')
    def make_published(self, request: HttpRequest, queryset: QuerySet[Post]) -> None:
        """
        Marks the selected posts as published via Admin Site.

        Args:
            self: The instance of the class.
            request: The HTTP request object.
            queryset: The queryset of posts to be marked as published.

        Returns:
            None

        Raises:
            None
        """
        if queryset.exists():
            updated = queryset.update(status='P')
            self.message_user(request, ngettext(
                '%d post was successfully marked as published.',
                '%d posts were successfully marked as published.',
                updated,
            ) % updated, messages.SUCCESS)
        else:
            self.message_user(request, "No posts were selected.", messages.WARNING)


class TagAdmin(admin.ModelAdmin):
    actions = None


# SECTION - Model and Model Admin Registration 
admin.site.register(model_or_iterable=Tag, admin_class=TagAdmin)
admin.site.register(model_or_iterable=Post, admin_class=PostAdmin)
admin.site.register(model_or_iterable=Comment)
