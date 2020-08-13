from django import forms
#from django.contrib.auth.models import User
from .models import *

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = '__all__'
        #exclude = ('data_criacao',)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
