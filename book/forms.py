from bson import ObjectId
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    # Agregar estilos a todos los elementos del formulario
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        for f in iter(self.fields):
            self.fields[f].widget.attrs.update({"class": "form-control"})

    # Agregar estilos por elementos del formulario
    class Meta:
        model = Book
        fields = ("name", "content", "category", "dimension")
        labels = {
            "name": "Nombre",
            "content": "Contenido",
            "category": "Categoría",
        }
        widgets = {
            "name": forms.TextInput({"placeholder": "El Quijote"}),
            "content": forms.Textarea(
                attrs={"rows": 5, "placeholder": "En un lugar de la mancha..."}),
            "category": forms.Select(
                attrs={"placeholder": "Elige una opción"}
            )
        }
        help_texts = {
            "content": "Escribe en este campo una breve descripción del libro"
        }

    def is_valid(self):
        self.data._mutable = True
        self.data["category"] = ObjectId(self.data["category"])

        # valid = super(BookForm, self).is_valid()

        return self.custom_valid_dimension()

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        instance.dimension = self.data["dimension"]

        if instance._id:
            book = Book.objects.get(pk=ObjectId(instance._id))
            self.data["dimension"]["_id"] = book.dimension["_id"]

        if commit:
            instance.save()

        return instance

    def custom_valid_dimension(self):
        if "dimension" in self.errors:
            del self.errors["dimension"]

            if len(self.errors) == 0:
                try:
                    self.data["dimension"] = {
                        "_id": ObjectId(),
                        "x": int(self.data["dimension-x"]),
                        "y": int(self.data["dimension-y"]),
                        "z": int(self.data["dimension-z"]),
                    }
                except ValueError:
                    self.add_error("dimension", "Al menos una dimensiones es inválida")
                    return False

                del self.data["dimension-x"]
                del self.data["dimension-y"]
                del self.data["dimension-z"]

                return True

        return False
