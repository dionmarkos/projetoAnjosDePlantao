from django import forms
from .models import *
from django.db import models
from django.utils import timezone
from django.forms import modelformset_factory

class CadastrarPessoaForm(forms.ModelForm):

    class Meta:
        model = Pessoa
        fields = ('nome', 'cpfCnpj', 'endereco', 'bairro', 'cidade', 'estado', 'telefone', 'observacoes', 'dataDeCadastro')

    def __init__(self, *args, **kwargs):
        super(CadastrarPessoaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'col form-control', 'placeholder' : 'Nome Completo'})
        self.fields['cpfCnpj'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Insira o CPF ou CNPJ'})
        self.fields['endereco'].widget.attrs.update({'class' : 'col-12 form-control', 'placeholder' : 'Rua, Nº e Complemento'})
        self.fields['bairro'].widget.attrs.update({'class' : 'col form-control', 'placeholder' : 'Bairro'})
        self.fields['cidade'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Cidade'})
        self.fields['estado'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Estado'})
        self.fields['telefone'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Telefone'})
        self.fields['observacoes'].widget.attrs.update({'class' : 'col-sm-8 form-control', 'style' : 'max-width: 500px; max-height: 100px;', 'placeholder' : 'Observações adicionais'})

class CadastrarProdutoForm(forms.ModelForm):
    class Meta:
        model = ProdutoDoacao
        fields = ('descricao',)

    def __init__(self, *args, **kwargs):
        super(CadastrarProdutoForm, self).__init__(*args, **kwargs)
        self.fields['descricao'].widget.attrs.update({'class' : 'col-md-6 form-control', 'placeholder' : 'Descrição do produto'})

class CaixaGeralForm(forms.ModelForm):

    class Meta:
        model = CaixaGeral
        fields = ('observacoes', 'saldo')

    def __init__(self, *args, **kwargs):
        super(CaixaGeralForm, self).__init__(*args, **kwargs)
        self.fields['observacoes'].widget.attrs.update({'class' : 'col-md-8 form-control', 'style' : 'height: 60px;', 'placeholder' : 'Observações importantes'})

class DoacaoEntradaForm(forms.ModelForm):
    valor = forms.CharField(widget=forms.TextInput(), required = False)
    quantiaDoacao = forms.CharField(widget=forms.TextInput(), required = False)
    class Meta:
        model = DoacaoEntrada
        fields = ('pessoa', 'valor', 'observacoes', 'quantiaDoacao', 'produtoDoacao')
    def __init__(self, *args, **kwargs):
        super(DoacaoEntradaForm, self).__init__(*args, **kwargs)
        self.fields['pessoa'].widget.attrs.update({'class':'custom-select', 'id':'inputGroupSelect01'})
        self.fields['produtoDoacao'].widget.attrs.update({'class':'col-8 custom-select', 'id':'inputGroupSelect01'})
        self.fields['observacoes'].widget.attrs.update({'class' : 'col-md-8 form-control', 'style' : 'height: 80px;', 'placeholder' : 'Observações sobre a doação'})
        self.fields['valor'].widget.attrs.update({'class': 'form-control col text-center','placeholder' : 'Ex: 100.00'})
        self.fields['quantiaDoacao'].widget.attrs.update({'class': 'form-control col-2 text-center w-auto','placeholder' : 'Quantidade'})
        self.fields["pessoa"].queryset = Pessoa.objects.filter(cadastro_ativo="Sim").order_by('nome')
        self.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.filter(cadastro_ativo="Sim").order_by('descricao')

class DoacaoSaidaForm(forms.ModelForm):
    valor = forms.CharField(widget=forms.TextInput(), required = False)
    quantiaDoacao = forms.CharField(widget=forms.TextInput(), required = False)
    class Meta:
        model = DoacaoSaida
        fields = ('pessoa', 'valor', 'observacoes',  'produtoDoacao', 'quantiaDoacao')
    def __init__(self, *args, **kwargs):
        super(DoacaoSaidaForm, self).__init__(*args, **kwargs)
        self.fields['pessoa'].widget.attrs.update({'class':'custom-select', 'id':'inputGroupSelect01'})
        self.fields['produtoDoacao'].widget.attrs.update({'class':'col-8 custom-select', 'id':'inputGroupSelect01'})
        self.fields['observacoes'].widget.attrs.update({'class' : 'col-md-8 form-control', 'style' : 'height: 80px;', 'placeholder' : 'Observações sobre a doação'})
        self.fields['valor'].widget.attrs.update({'class': 'form-control col text-center','placeholder' : 'Ex: 100.00'})
        self.fields['quantiaDoacao'].widget.attrs.update({'class': 'form-control col-2 text-center w-auto','placeholder' : 'Quantidade'})
        self.fields["pessoa"].queryset = Pessoa.objects.filter(cadastro_ativo="Sim").order_by('nome')
        self.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.filter(cadastro_ativo="Sim").order_by('descricao')

class BuscaForm(forms.ModelForm):
    class Meta:
        model = Busca
        fields = ('tipo_busca', 'texto_busca', 'status_cadastro')

    def __init__(self, *args, **kwargs):
        super(BuscaForm, self).__init__(*args, **kwargs)
        self.fields['status_cadastro'].widget.attrs.update({'class':'custom-select col-2', 'id':'status_cadastro'})
        self.fields['tipo_busca'].widget.attrs.update({'class':'custom-select col', 'id':'tipo_busca'})
        self.fields['texto_busca'].widget.attrs.update({'class' : 'col form-control w-auto', 'placeholder' : 'Ex: Maria Silva | Arrecadação na Praça etc'})
