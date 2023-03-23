from django.db import models
import PIL

# Create your models here.
class MyModel(models.Model):
    image = models.ImageField(upload_to='images/')