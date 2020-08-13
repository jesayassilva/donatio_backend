from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import date
from datetime import datetime

class Categoria(models.Model):
    descricao = models.CharField(max_length=50)
    def __str__(self):
        return str(self.descricao)

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria)
    nome = models.CharField(max_length=100)
    #descricao = model.TextField()
    #foto = model.ImageField()
    def __str__(self):
        return str(self.nome)

class Doacao(models.Model):
      doador = models.ForeignKey(User,related_name = 'doador',null = True)
      receptor = models.ForeignKey(User, null = True, blank = True, related_name = 'receptor')
      produto = models.ForeignKey(Produto, related_name = 'produto',null = True)
      #data_criacao = models.DateTimeField(default = timezone.now)
      data_criacao = models.DateTimeField(default=datetime.now)
      data_conclusao = models.DateField(null = True, blank = True)
      conclusao = models.BooleanField(default = False)
      #foto = models.CharField(max_length=1000,null=True,blank=True)
      foto = models.FileField()
      descricao = models.CharField(max_length=500, null = True, blank = True)
      def __str__(self):
          return str(self.descricao)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField(null = True)
    telefone1 = models.CharField(max_length=20)
    telefone2 = models.CharField(max_length=20)
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=30)
    endereco = models.CharField(max_length=300)
    tipo_usuario  = models.CharField(max_length=20)

@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
