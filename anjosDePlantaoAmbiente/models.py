# Create your models here.
from django.db import models
from django.utils import timezone
import pytz
import datetime

class Pessoa(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=50)
    cpfCnpj = models.CharField(max_length=14)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=60)
    estado = models.CharField(max_length=20)
    telefone = models.CharField(max_length=14)
    observacoes = models.TextField(blank=True)
    dataDeCadastro = models.DateTimeField(blank=True)

    def __str__(self):
        return '{} | CPF/CNPJ = {} | Bairro = {} | Cidade = {}'.format(self.nome, self.cpfCnpj, self.bairro, self.cidade)

    def get_type(self):
        return "Pessoa"

class ProdutoDoacao(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    dataDeCadastro = models.DateTimeField(default=timezone.now, null=True, blank=True)
    descricao = models.CharField(max_length=50, blank=False)
    saldoEstoque = models.DecimalField(max_digits=11, decimal_places=2, blank=True, default=0.0)

    def __str__(self):
        return '{} | Saldo de Estoque = {}'.format(self.descricao, self.saldoEstoque)

    def entrada_estoque(self, quantiaDoacao):
        self.saldoEstoque += quantiaDoacao
        self.save()
        return

    def saida_estoque(self, quantiaDoacao):
        if quantiaDoacao > self.saldoEstoque:
            messages.warning(request, 'Erro! Produto com saldo de estoque insuficiente. Digite uma quantia disponível.', extra_tags='alert alert-danger')
            return
        else:
            self.saldoEstoque -= quantiaDoacao
            self.save()
        return

    def entrada_estoque_detail(self, quantiaDoacao, doacao):
        pkAntigo = (doacao.pk)
        selfValorAntigo = DoacaoEntrada.objects.get(pk=pkAntigo)
        self.saldoEstoque -= selfValorAntigo.quantiaDoacao
        self.saldoEstoque += quantiaDoacao
        self.save()
        return

    def saida_estoque_detail(self, quantiaDoacao, doacao):
        if quantiaDoacao > self.saldoEstoque:
            messages.warning(request, 'Erro! Produto com saldo de estoque insuficiente. Digite uma quantia disponível.', extra_tags='alert alert-danger')
            return
        else:
            pkAntigo = (doacao.pk)
            selfValorAntigo = DoacaoSaida.objects.get(pk=pkAntigo)
            self.saldoEstoque += selfValorAntigo.quantiaDoacao
            self.saldoEstoque -= quantiaDoacao
            self.save()
        return

class DoacaoEntrada(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING)
    produtoDoacao = models.ForeignKey(ProdutoDoacao, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantiaDoacao = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, default=0)
    dataDoacao = models.DateTimeField(default=timezone.now, null=True, blank=True)
    valor = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    tipoDoacao = "Recebida"

    def __str__(self):
        return '{} | {} | Valor R$ = {} | Produto = {} | Quantia = {}'.format(self.dataDoacao.strftime("%d/%m/%Y %H:%M:%S"), self.pessoa.nome, self.valor, self.produtoDoacao.descricao, self.quantiaDoacao)

class DoacaoSaida(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.DO_NOTHING)
    produtoDoacao = models.ForeignKey(ProdutoDoacao, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantiaDoacao = models.DecimalField(max_digits=11, decimal_places=2, blank=True, default=0, null=True,)
    dataDoacao = models.DateTimeField(default=timezone.now, null=True, blank=True)
    valor = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    tipoDoacao = "Realizada"

class CaixaGeral(models.Model):
    autor = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    observacoes = models.TextField(blank=False)
    dataDeCadastro = models.DateTimeField(default=timezone.now, null=True, blank=True)
    saldo = models.DecimalField(max_digits=11, decimal_places=2)

    def entrada_saldo(self, valor):
        self.saldo += valor
        self.save()
        return

    def saida_saldo(self, valor):
        if valor > self.saldo:
            messages.warning(request, 'Erro! Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
            return
        else:
            self.saldo -= valor
            self.save()
        return

    def entrada_saldo_detail(self, valor, doacao):
        pkAntigo = (doacao.pk)
        selfValorAntigo = DoacaoEntrada.objects.get(pk=pkAntigo)
        self.saldo -= selfValorAntigo.valor
        self.saldo += valor
        self.save()
        return

    def saida_saldo_detail(self, valor, doacao):
        if valor > self.saldo:
            messages.warning(request, 'Erro! Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
            return
        else:
            pkAntigo = (doacao.pk)
            selfValorAntigo = DoacaoSaida.objects.get(pk=pkAntigo)
            self.saldo += selfValorAntigo.valor
            self.saldo -= valor
            self.save()
        return

class Busca(models.Model):
    TIPOS_DE_BUSCA = (
        ('pessoa', 'Pessoa'),
        ('evento', 'Evento'),
        ('produto', 'Produto'),
        ('usuario', 'Usuário'),
        ('doacao_entrada', 'Doações Recebidas'),
        ('doacao_saida', 'Doações Realizadas'),
    )
    tipo_busca = models.CharField(max_length=15, choices=TIPOS_DE_BUSCA, default='pessoa')
    texto_busca = models.CharField(max_length=30, blank=True)
