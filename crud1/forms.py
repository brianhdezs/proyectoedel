# forms.py
from django import forms
from .models import Usuario
from .models import Pelicula


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'contraseña', 'tipo_usuario', 'estado']

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'sinopsis', 'duracion', 'genero', 'estado', 'imagen', 'precio']