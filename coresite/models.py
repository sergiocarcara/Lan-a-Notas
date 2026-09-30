from django.db import models

# Create your models here.

class Nota(models.Model):
    nome_aluno = models.CharField(max_length=200)
    disciplina = models.CharField(max_length=200)
    nota_atividade = models.IntegerField(default=0)
    nota_trabalho = models.IntegerField(default=0)
    nota_prova = models.IntegerField(default=0)
    media = models.IntegerField(blank=True, default=0) 

    