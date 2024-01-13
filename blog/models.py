from django.db import models
from django.conf import settings
# Create your models here.

class Tag(models.Model):
  # Model Attrs
    value = models.TextField(max_length=100)

  # String Representation of Tag Model
  def __str__(self) -> str: 
    return str(self.value)
  


class Post(models.Model):
  author = models.Foreign