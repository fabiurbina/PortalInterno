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


class ReuniaoAgenda(models.Model):

    conta = models.ForeignKey(
        ContaHostinger,
        on_delete=models.CASCADE,
        related_name="reunioes"
    )

    uid = models.CharField(
        max_length=500,
        blank=True,
        default=""
    )

    titulo = models.TextField(
        blank=True,
        default=""
    )

    inicio = models.DateTimeField(
        null=True,
        blank=True
    )

    fim = models.DateTimeField(
        null=True,
        blank=True
    )

    inicio_formatado = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    fim_formatado = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    data = models.DateField(
        null=True,
        blank=True
    )

    hora_inicio = models.CharField(
        max_length=10,
        blank=True,
        default=""
    )

    hora_fim = models.CharField(
        max_length=10,
        blank=True,
        default=""
    )

    organizador_nome = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    organizador_email = models.EmailField(
        blank=True,
        default=""
    )

    participantes = models.JSONField(
        default=list,
        blank=True
    )

    link_reuniao = models.TextField(
        blank=True,
        default=""
    )

    local = models.TextField(
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    descricao = models.TextField(
        blank=True,
        default=""
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["conta", "uid"],
                name="unico_uid_por_conta"
            )
        ]

        ordering = [
            "inicio"
        ]

    def __str__(self):

        return (
            f"{self.conta.email} - "
            f"{self.titulo} - "
            f"{self.inicio}"
        )