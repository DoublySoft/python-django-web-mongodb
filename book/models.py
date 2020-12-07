from django import forms
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


class Dimension(models.Model):
    _id = models.ObjectIdField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()


class DimensionForm(forms.ModelForm):
    # Agregar estilos a todos los elementos del formulario
    def __init__(self, *args, **kwargs):
        super(DimensionForm, self).__init__(*args, **kwargs)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Dimension
        fields = ("x", "y", "z")


class Category(Base):
    class Meta:
        verbose_name_plural = "Categories"


class Address(models.Model):
    _id = models.ObjectIdField()
    direction = models.TextField()
    country = models.CharField(max_length=20)


class Tag(Base):
    pass


class Book(Base):
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dimension = models.EmbeddedField(model_container=Dimension, model_form_class=DimensionForm)
    addresses = models.ArrayField(model_container=Address)
    tags = models.ManyToManyField(Tag, through="Taggables", through_fields=("book", "tag"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Taggables(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
