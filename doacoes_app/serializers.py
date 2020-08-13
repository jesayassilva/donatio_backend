from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

#class ProdutoSerializer(serializers.Serializer):  Errado!

class ProdutoSerializer(serializers.ModelSerializer): # Certo!
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer): # Certo!
    class Meta:
        model = Categoria
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DoacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doacao
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'
