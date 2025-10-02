from django.db import models

# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Book(models.Model):
    author= models.ForeignKey(Author, null=True,on_delete=models.SET_NULL,related_name='books')
    title =models.CharField(max_length=100)
    price= models.IntegerField()
    rating=models.IntegerField(default=0)
    published=models.BooleanField(default=True)

