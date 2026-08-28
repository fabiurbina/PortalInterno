from django.db import models
from django.contrib.auth.models import User


class ContaHostinger(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="conta_hostinger"
    )

    email = models.EmailField()

    senha_criptografada = models.TextField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.usuario.username} - {self.email}"