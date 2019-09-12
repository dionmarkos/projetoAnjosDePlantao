from django.db import models
from django.utils import timezone

# Create your models here.
class Evento(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=50)
    data = models.DateTimeField()
    local = models.CharField(max_length=80)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=20)
    observacoes = models.TextField(blank=True)
    dataDeCadastro = models.DateTimeField(blank=True)
    cadastro_ativo = models.CharField(default="Sim", max_length=3, blank=True)
