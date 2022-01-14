from django.db import models
from colorfield.fields import ColorField
# Create your models here.


class ColorsPallete(models.Model):
    name  = models.CharField("Name" ,max_length= 20)
    image = models.ImageField(null = True , blank = True, upload_to = "images/")
    colorcode = ColorField()
    def __str__(self):
        return self.name

class LipsModel(models.Model):
    name  = models.CharField("Name" ,max_length= 20)
    image = models.ImageField(upload_to = "images/")
    colors = models.ManyToManyField(ColorsPallete,blank = True)

    def __str__(self):
        return self.name


class FaceModel(models.Model):
    name  = models.CharField("Name" ,max_length= 20)
    image = models.ImageField(upload_to = "images/")
    colors = models.ManyToManyField(ColorsPallete,blank = True)

    def __str__(self):
        return self.name

class EyesModel(models.Model):
    name  = models.CharField("Name" ,max_length= 20)
    image = models.ImageField(upload_to = "images/")
    colors = models.ManyToManyField(ColorsPallete,blank = True)

    def __str__(self):
        return self.name


class LooksModel(models.Model):
    name  = models.CharField("Name" ,max_length= 20)
    image = models.ImageField(upload_to = "images/")
    colors = models.ManyToManyField(ColorsPallete,blank = True)

    def __str__(self):
        return self.name
