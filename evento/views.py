from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import login

@login_required(login_url='/accounts/login/')
def cadastrar_evento(request):
    evento = None
    if request.method == "POST":
        formEvento = CadastrarEventoForm(request.POST)
        if formEvento.is_valid():
            evento = formEvento.save(commit=False)
            evento.nome = (evento.nome.title())
            evento.autor = request.user
            evento.dataDeCadastro = timezone.now()
            evento.save()
            messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
            return redirect('cadastrar_evento_detail', pk=evento.pk)
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formEvento = CadastrarEventoForm()
    return render(request, 'blog/cadastrar_evento.html', {'formEvento': formEvento, 'evento':evento})

@login_required(login_url='/accounts/login/')
def cadastrar_evento_detail(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if evento is not None:
        if request.method == "POST":
            formEvento = CadastrarEventoForm(request.POST, instance=evento)
            if formEvento.is_valid():
                evento = formEvento.save(commit=False)
                evento.nome = (evento.nome.title())
                evento.autor = request.user
                evento.dataDeCadastro = timezone.now()
                evento.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('cadastrar_evento_detail', pk=evento.pk)
        else:
            formEvento = CadastrarEventoForm(instance=evento)
    formEvento = CadastrarEventoForm(instance=evento)
    return render(request, 'blog/cadastrar_evento.html', {'formEvento': formEvento, 'evento':evento})
