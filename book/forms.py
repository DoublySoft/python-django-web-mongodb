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
        fields = ("name", "content", "category", "dimension", "addresses", "tags")
        labels = {
            "name": "Nombre",
            "content": "Contenido",
            "category": "Categoría",
            "dimension": "Dimensiónes",
            "addresses": "Dirección",
            "tags": "Etiquetas",
        }
        widgets = {
            "name": forms.TextInput({"placeholder": "El Quijote"}),
            "content": forms.Textarea(attrs={"rows": 5, "placeholder": "En un lugar de la mancha..."}),
            "category": forms.Select(attrs={"placeholder": "Elige una opción"})
        }
        help_texts = {
            "content": "Escribe en este campo una breve descripción del libro"
        }

    def is_valid(self):
        self.custom_valid_category()
        self.custom_valid_tags()

        valid = super(BookForm, self).is_valid()

        dimension = self.custom_valid_dimension()
        addresses = self.custom_valid_addresses()

        return len(self.errors) == 0

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)

        if instance._id:
            book = Book.objects.get(pk=ObjectId(instance._id))
            self.data["dimension"]["_id"] = book.dimension["_id"]
            instance.addresses = book.addresses
            instance.addresses.append(self.data["addresses"][0])
            instance.tags.set(self.data.getlist("tags"))
        else:
            instance.addresses = self.data["addresses"]

        instance.dimension = self.data["dimension"]

        if commit:
            instance.save()

        return instance

    # Convertir datos de un campo a ObjectId ForeignKey
    def custom_valid_category(self):
        self.data._mutable = True
        self.data["category"] = ObjectId(self.data["category"])

    # Convertir datos de un campo embebido One to One
    def custom_valid_dimension(self):
        if "dimension" in self.errors:
            del self.errors["dimension"]

            # if len(self.errors) == 0:
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

            # del self.data["dimension-x"]
            # del self.data["dimension-y"]
            # del self.data["dimension-z"]

            return True

        return False

    # Convertir datos de un campo embebido One to Many
    def custom_valid_addresses(self):
        if "addresses" in self.errors:
            del self.errors["addresses"]

            # if len(self.errors) == 0:

            if self.data["addresses-direction"].strip() == "" or self.data["addresses-country"].strip() == "":
                self.add_error("addresses", "Al menos un campo de la dirección es inválida")
                return False

            self.data["addresses"] = [
                {
                    "_id": ObjectId(),
                    "direction": self.data["addresses-direction"].strip(),
                    "country": self.data["addresses-country"].strip(),
                }
            ]

            del self.data["addresses-direction"]
            del self.data["addresses-country"]

            return True

        return False

    # Convertir datos a Many to Many de str a ObjectId
    def custom_valid_tags(self):
        # print(self.data.getlist("tags"))
        self.data.setlist("tags", list(map(lambda t_id: ObjectId(t_id), self.data.getlist("tags"))))
        # print(self.data.getlist("tags"))
