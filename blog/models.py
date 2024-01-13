from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Tag(models.Model):
  # Model Attrs:
    value = models.TextField(max_length=100)

  # String Representation of Tag Model
    def __str__(self) -> str: 
      return str(self.value)

class Post(models.Model):
  # Model Attrs:
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(""), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Written On"), auto_now_add=True)
    last_modified_at = models.DateTimeField(_("Last Updated On"), auto_now=True)
    published_at = models.DateTimeField(_("Posted On"), blank=True, null=True)
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts")

  # String Representation of Tag Model
    def __str__(self) -> str: 
      return str(self.title)