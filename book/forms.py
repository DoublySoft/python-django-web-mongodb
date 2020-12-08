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

        if 'dimension' in self.errors:
            del self.errors['dimension']

        if len(self.errors) == 0:
            self.data['dimension'] = {
                "_id": ObjectId(),
                "x": self.data['dimension-x'],
                "y": self.data['dimension-y'],
                "z": self.data['dimension-z'],
            }

            del self.data['dimension-x']
            del self.data['dimension-y']
            del self.data['dimension-z']

            return True

        # return super(BookForm, self).is_valid()
        return False

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        instance.dimension = self.data['dimension']

        if commit:
            instance.save()

        return instance
