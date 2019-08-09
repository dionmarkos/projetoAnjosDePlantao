from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from operator import attrgetter
from django.shortcuts import redirect
from evento.models import Evento
from django.db.models import Q
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def servicos(request):
    return render(request, 'blog/servicos.html', {})

@login_required(login_url='/accounts/login/')
def cadastrar_pessoa(request):
    pessoa = None
    if request.method == "POST":
        formCadastroPessoa = CadastrarPessoaForm(request.POST)
        if formCadastroPessoa.is_valid():
            pessoa = formCadastroPessoa.save(commit=False)
            pessoa.nome = (pessoa.nome.title())
            pessoa.autor = request.user
            pessoa.dataDeCadastro = timezone.now()
            pessoa.save()
            messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
            return redirect('cadastrar_pessoa_detail', pk=pessoa.pk)
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formCadastroPessoa = CadastrarPessoaForm()
    return render(request, 'blog/cadastrar_pessoa.html', {'formCadastroPessoa': formCadastroPessoa, 'pessoa':pessoa})

@login_required(login_url='/accounts/login/')
def cadastrar_pessoa_detail(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    if pessoa is not None:
        if request.method == "POST":
            formCadastroPessoa = CadastrarPessoaForm(request.POST, instance=pessoa)
            if formCadastroPessoa.is_valid():
                pessoa = formCadastroPessoa.save(commit=False)
                pessoa.nome = (pessoa.nome.title())
                pessoa.autor = request.user
                pessoa.dataDeCadastro = timezone.now()
                pessoa.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('cadastrar_pessoa_detail', pk=pessoa.pk)
        else:
            formCadastroPessoa = CadastrarPessoaForm(instance=pessoa)
    pessoas = Pessoa.objects.all()
    formCadastroPessoa = CadastrarPessoaForm(instance=pessoa)
    return render(request, 'blog/cadastrar_pessoa.html', {'formCadastroPessoa': formCadastroPessoa, 'pessoa':pessoa})

@login_required(login_url='/accounts/login/')
def cadastrar_produto(request):
    produto = None
    if request.method == "POST":
        formCadastroProduto = CadastrarProdutoForm(request.POST)
        if formCadastroProduto.is_valid():
            produto = formCadastroProduto.save(commit=False)
            produto.descricao = (produto.descricao.title())
            produto.autor = request.user
            produto.dataDeCadastro = timezone.now()
            produto.save()
            messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
            return redirect('cadastrar_produto_detail', pk=produto.pk)
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formCadastroProduto = CadastrarProdutoForm()
    formCadastroProduto = CadastrarProdutoForm()
    return render(request, 'blog/cadastrar_produto.html', {'formCadastroProduto': formCadastroProduto, 'produto':produto})

@login_required(login_url='/accounts/login/')
def cadastrar_produto_detail(request, pk):
    produto = get_object_or_404(ProdutoDoacao, pk=pk)
    if produto is not None:
        if request.method == "POST":
            formCadastroProduto = CadastrarProdutoForm(request.POST, instance=produto)
            if formCadastroProduto.is_valid():
                produto = formCadastroProduto.save(commit=False)
                produto.descricao = (produto.descricao.title())
                produto.autor = request.user
                produto.dataDeCadastro = timezone.now()
                produto.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('cadastrar_produto_detail', pk=produto.pk)
        else:
            formCadastroProduto = CadastrarProdutoForm(instance=produto)
    formCadastroProduto = CadastrarProdutoForm(instance=produto)
    return render(request, 'blog/cadastrar_produto.html', {'formCadastroProduto': formCadastroProduto, 'produto':produto})

@login_required(login_url='/accounts/login/')
def caixa_geral(request):
    operacao = None
    if request.method == "POST":
        formCaixaGeral = CaixaGeralForm(request.POST)
        if formCaixaGeral.is_valid():
            try:
                operacao = CaixaGeral.objects.all()[0]
                operacao.observacoes = formCaixaGeral['observacoes'].value()
                operacao.autor = request.user
                operacao.dataDeCadastro = timezone.now()
                operacao.save()
            except:
                operacao = formCaixaGeral.save(commit=False)
                operacao.autor = request.user
                operacao.dataDeCadastro = timezone.now()
                operacao.save()
            messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formCaixaGeral = CaixaGeralForm(instance=CaixaGeral.objects.all()[0])
    operacao = CaixaGeral.objects.all()[0]
    ultimasDoacoes = list(DoacaoEntrada.objects.all()[(len(DoacaoEntrada.objects.all())-7):])
    ultimasDoacoes += list(DoacaoSaida.objects.all()[(len(DoacaoSaida.objects.all())-7):])
    ultimasDoacoes.sort(key=lambda x: x.dataDoacao, reverse=True)
    return render(request, 'blog/caixa_geral.html', {'formCaixaGeral': formCaixaGeral, 'operacao':operacao, 'ultimasDoacoes':ultimasDoacoes})

@login_required(login_url='/accounts/login/')
def doacao_entrada(request):
    caixaGeral = None
    doacao = None
    if request.method == "POST":
        formDoacaoEntrada = DoacaoEntradaForm(request.POST)
        valor = formDoacaoEntrada['valor'].value()
        if float(valor) < 0.0:
            messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
        elif formDoacaoEntrada.is_valid():
            doacao = formDoacaoEntrada.save(commit=False)
            doacao.produtoDoacao.entrada_estoque(doacao.quantiaDoacao)
            doacao.autor = request.user
            doacao.dataDoacao = timezone.now()
            doacao.save()
            caixaGeral = CaixaGeral.objects.all()[0]
            caixaGeral.entrada_saldo(doacao.valor)
            messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
            return redirect('doacao_entrada_detail', pk=doacao.pk)
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formDoacaoEntrada = DoacaoEntradaForm()
    doacoes = DoacaoEntrada.objects.all()
    formDoacaoEntrada = DoacaoEntradaForm()
    formDoacaoEntrada.fields["pessoa"].queryset = Pessoa.objects.all().order_by('nome')
    formDoacaoEntrada.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.all().order_by('descricao')
    return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada, 'doacao':doacao})

@login_required(login_url='/accounts/login/')
def doacao_entrada_detail(request, pk):
    doacao = get_object_or_404(DoacaoEntrada, pk=pk)
    if doacao is not None:
        caixaGeral = None
        if request.method == "POST":
            formDoacaoEntrada = DoacaoEntradaForm(request.POST, instance=doacao)
            valor = formDoacaoEntrada['valor'].value()
            if float(valor) < 0.0:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
            elif formDoacaoEntrada.is_valid():
                doacao = formDoacaoEntrada.save(commit=False)
                doacao.produtoDoacao.entrada_estoque_detail(doacao.quantiaDoacao, doacao)
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                caixaGeral = CaixaGeral.objects.all()[0]
                caixaGeral.entrada_saldo_detail(doacao.valor, doacao)
                doacao.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_entrada_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoEntrada = DoacaoEntradaForm(instance=doacao)
    doacoes = DoacaoEntrada.objects.all()
    formDoacaoEntrada.fields["pessoa"].queryset = Pessoa.objects.all().order_by('nome')
    formDoacaoEntrada.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.all().order_by('descricao')
    return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada,'doacao':doacao})

@login_required(login_url='/accounts/login/')
def doacao_saida(request):
    caixaGeral = None
    doacao = None
    if request.method == "POST":
        formDoacaoSaida = DoacaoSaidaForm(request.POST)
        valor = formDoacaoSaida['valor'].value()
        if float(valor) < 0.0:
            messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
        elif formDoacaoSaida.is_valid():
            caixaGeral = CaixaGeral.objects.all()[0]
            doacao = formDoacaoSaida.save(commit=False)
            if doacao.valor > caixaGeral.saldo:
                messages.warning(request, 'Erro! Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
                return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
            else:
                doacao.produtoDoacao.saida_estoque(doacao.quantiaDoacao)
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                doacao.save()
                caixaGeral.saida_saldo(doacao.valor)
                messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_saida_detail', pk=doacao.pk)
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formDoacaoSaida = DoacaoSaidaForm()
    formDoacaoSaida = DoacaoSaidaForm()
    doacoes = DoacaoSaida.objects.all()
    formDoacaoSaida.fields["pessoa"].queryset = Pessoa.objects.all().order_by('nome')
    formDoacaoSaida.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.all().order_by('descricao')
    return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida, 'doacao':doacao})

@login_required(login_url='/accounts/login/')
def doacao_saida_detail(request, pk):
    doacao = get_object_or_404(DoacaoSaida, pk=pk)
    if doacao is not None:
        caixaGeral = None
        if request.method == "POST":
            formDoacaoSaida = DoacaoSaidaForm(request.POST, instance=doacao)
            valor = formDoacaoSaida['valor'].value()
            if float(valor) < 0.0:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
            elif formDoacaoSaida.is_valid():
                caixaGeral = CaixaGeral.objects.all()[0]
                doacao = formDoacaoSaida.save(commit=False)
                if doacao.valor > caixaGeral.saldo:
                    messages.warning(request, 'Erro! Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
                    return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
                else:
                    doacao.produtoDoacao.saida_estoque_detail(doacao.quantiaDoacao, doacao)
                    doacao.autor = request.user
                    doacao.dataDoacao = timezone.now()
                    caixaGeral.saida_saldo_detail(doacao.valor, doacao)
                    doacao.save()
                    messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                    return redirect('doacao_saida_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoSaida = DoacaoSaidaForm(instance=doacao)
    formDoacaoSaida = DoacaoSaidaForm(instance=doacao)
    doacoes = DoacaoSaida.objects.all()
    formDoacaoSaida.fields["pessoa"].queryset = Pessoa.objects.all().order_by('nome')
    formDoacaoSaida.fields["produtoDoacao"].queryset = ProdutoDoacao.objects.all().order_by('descricao')
    return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida, 'doacao':doacao})

@login_required(login_url='/accounts/login/')
def busca(request, pk=0):
    resultados = None
    classeRetorno = None
    if request.method == "GET" and pk != 1:
        formBusca = BuscaForm(request.GET)
        if formBusca.is_valid():
            busca = formBusca.save(commit=False)

            if busca.tipo_busca == 'pessoa':
                classeRetorno = 'Pessoa'
                if busca.texto_busca is None:
                    resultados = Pessoa.objects.all().order_by('nome')
                else:
                    resultados = Pessoa.objects.filter(Q(nome__contains=busca.texto_busca) | Q(cpfCnpj__contains=busca.texto_busca) | Q(endereco__contains=busca.texto_busca) |
                    Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca) | Q(estado__contains=busca.texto_busca)).order_by('nome')

            elif busca.tipo_busca == 'evento':
                classeRetorno = 'Evento'
                if busca.texto_busca is None:
                    resultados = Evento.objects.all()
                else:
                    resultados = Evento.objects.filter(Q(nome__contains=busca.texto_busca) | Q(local__contains=busca.texto_busca)
                    | Q(endereco__contains=busca.texto_busca) | Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca)
                    | Q(estado__contains=busca.texto_busca)).order_by('dataDeCadastro').reverse()

            elif busca.tipo_busca == 'produto':
                classeRetorno = 'Produto'
                if busca.texto_busca is None:
                    resultados = ProdutoDoacao.objects.all()
                else:
                    resultados = ProdutoDoacao.objects.filter(descricao__contains=busca.texto_busca)

            elif busca.tipo_busca == 'usuario':
                classeRetorno = 'Usuario'
                if busca.texto_busca is None:
                    resultados = User.objects.all()
                else:
                    resultados = User.objects.filter(username__contains=busca.texto_busca)

            elif busca.tipo_busca == 'doacao_entrada':
                classeRetorno = 'DoacaoEntrada'
                if busca.texto_busca is None:
                    resultados = DoacaoEntrada.objects.all()
                else:
                    resultados = DoacaoEntrada.objects.filter(Q(pessoa__nome__contains=busca.texto_busca) | Q(pessoa__cpfCnpj__contains=busca.texto_busca) | Q(produtoDoacao__descricao__contains=busca.texto_busca)).order_by('dataDoacao').reverse()

            elif busca.tipo_busca == 'doacao_saida':
                classeRetorno = 'DoacaoSaida'
                if busca.texto_busca is None:
                    resultados = DoacaoSaida.objects.all()
                else:
                    resultados = DoacaoSaida.objects.filter(Q(pessoa__nome__contains=busca.texto_busca) | Q(pessoa__cpfCnpj__contains=busca.texto_busca) | Q(produtoDoacao__descricao__contains=busca.texto_busca)).order_by('dataDoacao').reverse()

            elif resultados.count() <= 0:
                messages.warning(request, 'Nenhum resultado encontrada com este parâmetro.', extra_tags='alert alert-warning')

            messages.success(request, 'Consulta realizada com sucesso!', extra_tags='alert alert-success')
        else:
            messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
    else:
        formBusca = BuscaForm()
    return render(request, 'blog/busca.html', {'formBusca': formBusca, 'resultados':resultados, 'classeRetorno':classeRetorno})
