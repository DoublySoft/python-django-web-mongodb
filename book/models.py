from djongo import models


class Book(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    content = models.TextField()

    @property
    def pk(self):
        return self._id

    def __str__(self):
        return self.name
