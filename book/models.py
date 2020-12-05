from djongo import models


class Book(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    content = models.TextField()
