from djongo import models


class Base(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=125)

    @property
    def pk(self):
        return self._id

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(Base):
    class Meta:
        verbose_name_plural = "Categories"


class Book(Base):
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
