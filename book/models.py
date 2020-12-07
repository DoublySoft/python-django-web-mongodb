from djongo import models


class Category(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    @property
    def pk(self):
        return self._id

    def __str__(self):
        return self.name


class Book(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=125)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def pk(self):
        return self._id

    def __str__(self):
        return self.name
