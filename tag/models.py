from random import SystemRandom
import string
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)