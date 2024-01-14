"""
Module Docstring: models.py

This module contains the definition of the Tag and Post models for the application.

Tag Model:
- The Tag model represents a tag that can be associated with a post.
- It has a single attribute 'value' which is a TextField and serves as the primary key.
- The model also includes a custom string representation method.

Post Model:
- The Post model represents a blog post.
- It includes various attributes such as author, title, content, status, and tags.
- The model also includes a custom string representation method.

Both models make use of the TypedModelMeta class for meta options and include indexes and constraints for database optimization.
"""

from django.conf import settings
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    # Model Attrs:
    value = models.TextField(max_length=100, primary_key=True)

    # String Representation of Tag Model
    def __str__(self) -> str:
        return str(self.value)

    class Meta(TypedModelMeta):
        db_table = "blog_tags"
        order_with_respect_to = "value"
        indexes = [
            models.Index(fields=["value"], name="tag_value"),
        ]
        constraints = [
      UniqueConstraint(Lower("value").desc(), name="unique_lower_name_tag")
]

class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta(TypedModelMeta):
        db_table = "blog_comments"

class Post(models.Model):
    class STATUS(models.TextChoices):
        DRAFT = "D", _("Draft")
        APPROVED = "P", _("Published")
        REJECTED = "W", _("Withdrawn")
    # Model Attrs:
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Post Creator"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Written On"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("Last Updated On"), auto_now=True)
    published_at = models.DateTimeField(_("Posted On"), blank=True, null=True)
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.TextField(max_length=500)
    content = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS.choices, default=STATUS.DRAFT) 
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation(Comment)
    # String Representation of Tag Model
    def __str__(self) -> str:
        return str(self.title)

    class Meta(TypedModelMeta):
        db_table = "blog_posts"
        ordering = ["-last_modified_at"]
        indexes = [
            models.Index(fields=["author"], name="post_author"),
            models.Index(fields=["status"], name="posts_status")
        ]
