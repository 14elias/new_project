from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
# Create your models here.
class LikedItems(models.Model):
    User=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.IntegerField()
    content_object=GenericForeignKey()