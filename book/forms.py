from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    # Agregar estilos Bootstrap cómo en el tutorial
    # def __init__(self, *args, **kwargs):
    #     super(BookForm, self).__init__(*args, **kwargs)
    #
    #     for f in iter(self.fields):
    #         self.fields[f].widget.attrs.update({'class': 'form-control'})

    # Agregar estilos Bootstrap de forma general
    class Meta:
        model = Book
        fields = ('name', 'content')
        labels = {
            'name': 'Nombre',
            'content': 'Contenido',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'El Quijote'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'En un lugar de la mancha...'}),
        }
        help_texts = {
            'content': 'Escribe en este campo una breve descripción del libro'
        }

# Agregar estilos Bootstrap por campo
# class BookForm(forms.Form):
#     name = forms.CharField(
#         label='Nombre',
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'El Quijote'}),
#     )
#     content = forms.CharField(
#         label='Contenido',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'En un lugar de la mancha...'}),
#         help_text='Escribe en este campo una breve descripción del libro'
#     )
