from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Product(models.Model):
        title = models.CharField(max_length=50)
        description = models.CharField(max_length=255)
        price = models.CharField(max_length=50)
        category = models.CharField(max_length=50)
        image = image = models.URLField(max_length=200) 