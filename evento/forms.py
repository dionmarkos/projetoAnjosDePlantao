from django import forms
from .models import *
from django.db import models
from django.utils import timezone

class CadastrarEventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = ('nome', 'data', 'bairro', 'local', 'endereco', 'cidade', 'estado', 'observacoes')

    def __init__(self, *args, **kwargs):
        super(CadastrarEventoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'col form-control', 'placeholder' : 'Nome do evento'})
        self.fields['data'].widget.attrs.update({'class' : 'col form-control datetimepicker-input', 'data-target' : '#datetimepicker1', 'placeholder':'DD/MM/AAAA HH:MM'})
        self.fields['local'].widget.attrs.update({'class' : 'col form-control', 'placeholder' : 'Local de realização'})
        self.fields['endereco'].widget.attrs.update({'class' : 'col-12 form-control', 'placeholder' : 'Rua, Nº e Complemento'})
        self.fields['bairro'].widget.attrs.update({'class' : 'col form-control', 'placeholder' : 'Bairro'})
        self.fields['cidade'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Cidade'})
        self.fields['estado'].widget.attrs.update({'class' : 'col-md-auto form-control', 'placeholder' : 'Estado'})
        self.fields['observacoes'].widget.attrs.update({'class' : 'col-sm-8 form-control', 'style' : 'max-width: 500px; max-height: 100px;', 'placeholder' : 'Observações adicionais'})
