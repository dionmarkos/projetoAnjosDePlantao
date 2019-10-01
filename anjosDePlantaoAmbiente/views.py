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
    try:
        if request.method == "POST":
            formCadastroPessoa = CadastrarPessoaForm(request.POST)
            if formCadastroPessoa.is_valid():
                pessoa = formCadastroPessoa.save(commit=False)
                # atualiza a primeira letra de cada nome com maiúscula
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
        return render(request, 'blog/cadastrar_pessoa.html', {'formCadastroPessoa': formCadastroPessoa})
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('cadastrar_pessoa')

@login_required(login_url='/accounts/login/')
def cadastrar_pessoa_detail(request, pk):
    try:
        pessoa = get_object_or_404(Pessoa, pk=pk)
        if request.method == "POST":
            formCadastroPessoa = CadastrarPessoaForm(request.POST, instance=pessoa)
            if formCadastroPessoa.is_valid():
                pessoa = formCadastroPessoa.save(commit=False)
                # atualiza a primeira letra de cada nome com maiúscula
                pessoa.nome = (pessoa.nome.title())
                pessoa.autor = request.user
                pessoa.dataDeCadastro = timezone.now()
                pessoa.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('cadastrar_pessoa_detail', pk=pessoa.pk)
        else:
            formCadastroPessoa = CadastrarPessoaForm(instance=pessoa)
        return render(request, 'blog/cadastrar_pessoa.html', {'formCadastroPessoa': formCadastroPessoa, 'pessoa':pessoa})
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('cadastrar_pessoa_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def cadastrar_pessoa_inativacao(request, pk):
    try:
        pessoa = get_object_or_404(Pessoa, pk=pk)
        if pessoa.cadastro_ativo == "Sim":
            pessoa.cadastro_ativo = "Não"
            messages.success(request, 'Cadastro inativado com sucesso!', extra_tags='alert alert-success')
        else:
            pessoa.cadastro_ativo = "Sim"
            messages.success(request, 'Cadastro ativado com sucesso!', extra_tags='alert alert-success')
        pessoa.save()
        return redirect('busca', pk=1)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('busca', pk=1)

@login_required(login_url='/accounts/login/')
def cadastrar_produto(request):
    try:
        if request.method == "POST":
            formCadastroProduto = CadastrarProdutoForm(request.POST)
            if formCadastroProduto.is_valid():
                produto = formCadastroProduto.save(commit=False)
                # atualiza a primeira letra de cada nome com maiúscula
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
        return render(request, 'blog/cadastrar_produto.html', {'formCadastroProduto': formCadastroProduto})
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('cadastrar_produto')

@login_required(login_url='/accounts/login/')
def cadastrar_produto_detail(request, pk):
    try:
        produto = get_object_or_404(ProdutoDoacao, pk=pk)
        if produto is not None:
            if request.method == "POST":
                formCadastroProduto = CadastrarProdutoForm(request.POST, instance=produto)
                if formCadastroProduto.is_valid():
                    produto = formCadastroProduto.save(commit=False)
                    # atualiza a primeira letra de cada nome com maiúscula
                    produto.descricao = (produto.descricao.title())
                    produto.autor = request.user
                    produto.dataDeCadastro = timezone.now()
                    produto.save()
                    messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                    return redirect('cadastrar_produto_detail', pk=produto.pk)
            else:
                formCadastroProduto = CadastrarProdutoForm(instance=produto)
        return render(request, 'blog/cadastrar_produto.html', {'formCadastroProduto': formCadastroProduto, 'produto':produto})
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('cadastrar_produto_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def cadastrar_produto_delete(request, pk):
    try:
        produto = get_object_or_404(ProdutoDoacao, pk=pk)
        if produto.cadastro_ativo == "Sim":
            produto.cadastro_ativo = "Não"
            messages.success(request, 'Cadastro inativado com sucesso!', extra_tags='alert alert-success')
        else:
            produto.cadastro_ativo = "Sim"
            messages.success(request, 'Cadastro ativado com sucesso!', extra_tags='alert alert-success')
        produto.save()
        return redirect('busca', pk=1)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('busca', pk=1)

@login_required(login_url='/accounts/login/')
def caixa_geral(request):
    try:
        operacao = None
        ultimasDoacoes = []
        if request.method == "POST":
            formCaixaGeral = CaixaGeralForm(request.POST)
            if formCaixaGeral.is_valid():
                # verifica se o objeto único do caixa geral já existe
                if len(CaixaGeral.objects.all()) > 0:
                    operacao = CaixaGeral.objects.all()[0]
                    operacao.observacoes = formCaixaGeral['observacoes'].value()
                    operacao.autor = request.user
                    operacao.dataDeCadastro = timezone.now()
                    operacao.save()
                else:
                    operacao = formCaixaGeral.save(commit=False)
                    operacao.autor = request.user
                    operacao.dataDeCadastro = timezone.now()
                    operacao.save()
                messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
                formCaixaGeral = CaixaGeralForm(instance=CaixaGeral.objects.all()[0])
                return render(request, 'blog/caixa_geral.html', {'formCaixaGeral': formCaixaGeral})
        else:
            # verifica se o objeto único do caixa geral já existe
            if len(CaixaGeral.objects.all()) > 0:
                formCaixaGeral = CaixaGeralForm(instance=CaixaGeral.objects.all()[0])
                operacao = CaixaGeral.objects.all()[0]
            else:
                formCaixaGeral = CaixaGeralForm()
        # lista das últimas doações realizadas ou recebidas, tendo no máximo 14 resultados
        # deve ser 7 recebidas e 7 realizadas
        # como devem ser 14 resultados, 7 de cada, precisa ver antes se existe esses 7 objetos
        if( len(DoacaoEntrada.objects.all()) > 7 ):
            # usa-se o len() para pegar apenas os 7 últimos objetos criados
            ultimasDoacoes = list(DoacaoEntrada.objects.all()[ (len(DoacaoEntrada.objects.all())-7 ):])
        else:
            # caso não houver os 7 objetos, retorna todos
            ultimasDoacoes = list(DoacaoEntrada.objects.all())
        if(len(DoacaoSaida.objects.all()) > 7):
            ultimasDoacoes += list(DoacaoSaida.objects.all()[ (len(DoacaoSaida.objects.all())-7 ):])
        else:
            ultimasDoacoes = list(DoacaoSaida.objects.all())
        # ordena os resultados da lista em ordem decrescente da data
        ultimasDoacoes.sort(key=lambda x: x.dataDoacao, reverse=True)
        produtos = ProdutoDoacao.objects.all()
        return render(request, 'blog/caixa_geral.html', {'formCaixaGeral': formCaixaGeral, 'operacao':operacao, 'ultimasDoacoes':ultimasDoacoes, 'produtos':produtos})
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('caixa_geral')

@login_required(login_url='/accounts/login/')
def doacao_entrada(request):
    try:
        if request.method == "POST":
            formDoacaoEntrada = DoacaoEntradaForm(request.POST)
            # verifica se os valores são maiores que zero
            valor = formDoacaoEntrada['valor'].value()
            quantiaDoacao = formDoacaoEntrada['quantiaDoacao'].value()
            if float(valor) < 0.00 or float(quantiaDoacao) < 0.00:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
                return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada})
            elif formDoacaoEntrada.is_valid():
                doacao = formDoacaoEntrada.save(commit=False)
                # verifica se o valor está zerado e o produto também
                if float(valor) <= 0.00 and doacao.produtoDoacao is None:
                    messages.warning(request, 'Erro! A doação precisa obrigatoriamente ter um valor ou um produto a ser doado.', extra_tags='alert alert-danger')
                    return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada})
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                doacao.save()
                # verifica se o produto a ser doado não é nulo, para fazer entrada de estoque
                if doacao.produtoDoacao is not None:
                    doacao.produtoDoacao.entrada_estoque(doacao.quantiaDoacao)
                    produtoDoado = ProdutoDoadoEntrada()
                    produtoDoado.produto = doacao.produtoDoacao
                    produtoDoado.quantidade = doacao.quantiaDoacao
                    produtoDoado.doacaoReferenciaPK = doacao.pk
                    produtoDoado.save()
                caixaGeral = CaixaGeral.objects.all()[0]
                caixaGeral.entrada_saldo(doacao.valor)
                messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_entrada_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoEntrada = DoacaoEntradaForm()
        return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada})
    except ValueError as excecao:
        messages.warning(request, 'Ops, algo deu errado. Parece que há algum campo vazio, foi digitado vírgula ao invés do ponto, ou houve algum outro problema. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_entrada')
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_entrada')

@login_required(login_url='/accounts/login/')
def doacao_entrada_detail(request, pk):
    try:
        doacao = get_object_or_404(DoacaoEntrada, pk=pk)
        if request.method == "POST":
            formDoacaoEntrada = DoacaoEntradaForm(request.POST, instance=doacao)
            # verifica se os valores são maiores que zero
            valor = formDoacaoEntrada['valor'].value()
            quantiaDoacao = formDoacaoEntrada['quantiaDoacao'].value()
            if float(valor) < 0.00 or float(quantiaDoacao) < 0.00:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
                return redirect('doacao_entrada_detail', pk=doacao.pk)
            elif formDoacaoEntrada.is_valid():
                doacao = formDoacaoEntrada.save(commit=False)
                # verifica se o valor está zerado e o produto também
                if float(valor) <= 0.00 and doacao.produtoDoacao is None:
                    messages.warning(request, 'Erro! A doação precisa obrigatoriamente ter um valor ou um produto a ser doado.', extra_tags='alert alert-danger')
                    return redirect('doacao_entrada_detail', pk=doacao.pk)
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                # verifica se o produto a ser doado não é nulo, para fazer entrada de estoque
                if doacao.produtoDoacao is not None:
                    doacao.produtoDoacao.entrada_estoque(doacao.quantiaDoacao)
                    produtoDoado = ProdutoDoadoEntrada()
                    produtoDoado.produto = doacao.produtoDoacao
                    produtoDoado.quantidade = doacao.quantiaDoacao
                    produtoDoado.doacaoReferenciaPK = doacao.pk
                    produtoDoado.save()
                caixaGeral = CaixaGeral.objects.all()[0]
                caixaGeral.entrada_saldo_detail(doacao.valor, doacao)
                doacao.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_entrada_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoEntrada = DoacaoEntradaForm(instance=doacao)
            produtosDoacao = ProdutoDoadoEntrada.objects.filter(doacaoReferenciaPK=pk)
        return render(request, 'blog/doacao_entrada.html', {'formDoacaoEntrada': formDoacaoEntrada, 'doacao':doacao, 'produtosDoacao':produtosDoacao})
    except ValueError as excecao:
        messages.warning(request, 'Ops, algo deu errado. Parece que há algum campo vazio, foi digitado vírgula ao invés do ponto, ou houve algum outro problema. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_entrada_detail', pk=pk)
    except Exception as excecao:
        messages.warning(request, 'Ops, algum erro aconteceu. Verifique os valores digitados e tente novamente. Se o problema persistir, entre com contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_entrada_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def doacao_entrada_delete(request, pk):
    try:
        doacao = get_object_or_404(DoacaoEntrada, pk=pk)
        # antes de deletar, retirar os saldos do estoque
        produtosDoacao = ProdutoDoadoEntrada.objects.filter(doacaoReferenciaPK=doacao.pk)
        for produtoDoacao in produtosDoacao:
            produtoDoacao.produto.saida_estoque(produtoDoacao.quantidade)
        # antes de deletar, retirar o saldo do caixa
        caixaGeral = CaixaGeral.objects.all()[0]
        caixaGeral.saida_saldo(doacao.valor)
        doacao.delete()
        messages.success(request, 'Excluído com sucesso!', extra_tags='alert alert-success')
        return redirect('busca', pk=1)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('busca', pk=1)

@login_required(login_url='/accounts/login/')
def doacao_entrada_delete_produto(request, pk):
    try:
        produtoDoado = get_object_or_404(ProdutoDoadoEntrada, pk=pk)
        pk = produtoDoado.doacaoReferenciaPK
        # antes de deletar, retirar os saldos do estoque
        produtoDoado.produto.saida_estoque(produtoDoado.quantidade)
        produtoDoado.delete()
        messages.success(request, 'Excluído com sucesso!', extra_tags='alert alert-success')
        return redirect('doacao_entrada_detail', pk=pk)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_entrada_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def doacao_saida(request):
    try:
        if request.method == "POST":
            formDoacaoSaida = DoacaoSaidaForm(request.POST)
            # verifica se os valores são maiores que zero
            valor = formDoacaoSaida['valor'].value()
            quantiaDoacao = formDoacaoSaida['quantiaDoacao'].value()
            if float(valor) < 0.00 or float(quantiaDoacao) < 0.00:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
                return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
            elif formDoacaoSaida.is_valid():
                caixaGeral = CaixaGeral.objects.all()[0]
                doacao = formDoacaoSaida.save(commit=False)
                # verifica se o valor está zerado e o produto também
                if float(valor) <= 0.00 and doacao.produtoDoacao is None:
                    messages.warning(request, 'Erro! A doação precisa obrigatoriamente ter um valor ou um produto a ser doado.', extra_tags='alert alert-danger')
                    return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
                # verifica se tem saldo suficiente em valor para doação
                if doacao.valor > caixaGeral.saldo:
                    messages.warning(request, 'Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
                    return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                doacao.save()
                caixaGeral.saida_saldo(doacao.valor)
                # verifica se o produto a ser doado não é nulo, para fazer saída de estoque
                if doacao.produtoDoacao is not None:
                    # verifica se tem saldo de estoque disponível (a função retorna True ou False - verificar)
                    if not doacao.produtoDoacao.saida_estoque(doacao.quantiaDoacao):
                        messages.warning(request, 'Produto com saldo de estoque insuficiente. Digite uma quantidade disponível.', extra_tags='alert alert-danger')
                        doacao.delete()
                        return redirect('doacao_saida')
                    produtoDoado = ProdutoDoadoSaida()
                    produtoDoado.produto = doacao.produtoDoacao
                    produtoDoado.quantidade = doacao.quantiaDoacao
                    produtoDoado.doacaoReferenciaPK = doacao.pk
                    produtoDoado.save()
                messages.success(request, 'Operação efetuada com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_saida_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoSaida = DoacaoSaidaForm()
        return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida})
    except ValueError as excecao:
        messages.warning(request, 'Ops, algo deu errado. Parece que há algum campo vazio, foi digitado vírgula ao invés do ponto, ou houve algum outro problema. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_saida')
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_saida')

@login_required(login_url='/accounts/login/')
def doacao_saida_detail(request, pk):
    try:
        doacao = get_object_or_404(DoacaoSaida, pk=pk)
        if request.method == "POST":
            formDoacaoSaida = DoacaoSaidaForm(request.POST, instance=doacao)
            # verifica se os valores são maiores que zero
            valor = formDoacaoSaida['valor'].value()
            quantiaDoacao = formDoacaoSaida['quantiaDoacao'].value()
            if float(valor) < 0.00 or float(quantiaDoacao) < 0.00:
                messages.warning(request, 'Erro! Insira um valor maior ou igual a zero.', extra_tags='alert alert-danger')
                return redirect('doacao_saida_detail', pk=doacao.pk)
            elif formDoacaoSaida.is_valid():
                caixaGeral = CaixaGeral.objects.all()[0]
                doacao = formDoacaoSaida.save(commit=False)
                # verifica se o valor está zerado e o produto também
                if float(valor) <= 0.00 and doacao.produtoDoacao is None:
                    messages.warning(request, 'Erro! A doação precisa obrigatoriamente ter um valor ou um produto a ser doado.', extra_tags='alert alert-danger')
                    return redirect('doacao_saida_detail', pk=doacao.pk)
                # verifica se tem saldo suficiente em valor para doação
                if doacao.valor > caixaGeral.saldo:
                    messages.warning(request, 'Erro! Saldo insuficiente. Digite um valor disponível.', extra_tags='alert alert-danger')
                    return redirect('doacao_saida_detail', pk=pk)
                doacao.autor = request.user
                doacao.dataDoacao = timezone.now()
                caixaGeral.saida_saldo_detail(doacao.valor, doacao)
                doacao.save()
                # verifica se o produto a ser doado não é nulo, para fazer saída de estoque
                if doacao.produtoDoacao is not None:
                    # verifica se tem saldo de estoque disponível (a função retorna True ou False - verificar)
                    if not doacao.produtoDoacao.saida_estoque(doacao.quantiaDoacao):
                        messages.warning(request, 'Produto com saldo de estoque insuficiente. Digite uma quantidade disponível.', extra_tags='alert alert-danger')
                        return redirect('doacao_saida_detail', pk=doacao.pk)
                    produtoDoado = ProdutoDoadoSaida()
                    produtoDoado.produto = doacao.produtoDoacao
                    produtoDoado.quantidade = doacao.quantiaDoacao
                    produtoDoado.doacaoReferenciaPK = doacao.pk
                    produtoDoado.save()
                messages.success(request, 'Cadastro atualizado com sucesso!', extra_tags='alert alert-success')
                return redirect('doacao_saida_detail', pk=doacao.pk)
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formDoacaoSaida = DoacaoSaidaForm(instance=doacao)
            produtosDoacao = ProdutoDoadoSaida.objects.filter(doacaoReferenciaPK=pk)
        return render(request, 'blog/doacao_saida.html', {'formDoacaoSaida': formDoacaoSaida, 'doacao':doacao, 'produtosDoacao':produtosDoacao})
    except ValueError as excecao:
        messages.warning(request, 'Ops, algo deu errado. Parece que há algum campo vazio, foi digitado vírgula ao invés do ponto, ou houve algum outro problema. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_saida_detail', pk=pk)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os valores digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_saida_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def doacao_saida_delete(request, pk):
    try:
        doacao = get_object_or_404(DoacaoSaida, pk=pk)
        # antes de deletar, voltar os saldos do estoque
        produtosDoacao = ProdutoDoadoSaida.objects.filter(doacaoReferenciaPK=doacao.pk)
        for produtoDoacao in produtosDoacao:
            produtoDoacao.produto.entrada_estoque(produtoDoacao.quantidade)
        # antes de deletar, voltar o saldo do caixa
        caixaGeral = CaixaGeral.objects.all()[0]
        caixaGeral.entrada_saldo(doacao.valor)
        doacao.delete()
        messages.success(request, 'Excluído com sucesso!', extra_tags='alert alert-success')
        return redirect('busca', pk=1)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('busca', pk=1)

@login_required(login_url='/accounts/login/')
def doacao_saida_delete_produto(request, pk):
    try:
        produtoDoado = get_object_or_404(ProdutoDoadoSaida, pk=pk)
        pk = produtoDoado.doacaoReferenciaPK
        # antes de deletar, retirar os saldos do estoque
        produtoDoado.produto.entrada_estoque(produtoDoado.quantidade)
        produtoDoado.delete()
        messages.success(request, 'Excluído com sucesso!', extra_tags='alert alert-success')
        return redirect('doacao_saida_detail', pk=pk)
    except Exception as excecao:
        messages.warning(request, 'Ops, algo deu errado. Verifique os dados digitados e tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        return redirect('doacao_saida_detail', pk=pk)

@login_required(login_url='/accounts/login/')
def busca(request, pk=0):
    try:
        resultados = None
        classeRetorno = None
        busca = None
        produtosDoacao = ProdutoDoadoEntrada.objects.none()
        # como todos as requisições de busca são GET, necessita do pk=1, para não retornar o alert de erro
        # que contém no penúltimo else, caso contrário, no primeiro acesso já retorna alert de erro
        # e também após deletar ou inativar um cadastro, retorna erro de validação do form
        if request.method == "GET" and pk != 1:
            formBusca = BuscaForm(request.GET)
            if formBusca.is_valid():
                busca = formBusca.save(commit=False)

                if busca.tipo_busca == 'pessoa':
                    classeRetorno = 'Pessoa'
                    if busca.status_cadastro == 'ativo':
                        resultados = Pessoa.objects.filter(Q(nome__contains=busca.texto_busca) | Q(cpfCnpj__contains=busca.texto_busca) | Q(endereco__contains=busca.texto_busca) |
                        Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca) | Q(estado__contains=busca.texto_busca)).order_by('nome').exclude(Q(cadastro_ativo="Não"))
                    else:
                        resultados = Pessoa.objects.filter(Q(nome__contains=busca.texto_busca) | Q(cpfCnpj__contains=busca.texto_busca) | Q(endereco__contains=busca.texto_busca) |
                        Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca) | Q(estado__contains=busca.texto_busca)).order_by('nome').exclude(Q(cadastro_ativo="Sim"))

                elif busca.tipo_busca == 'evento':
                    classeRetorno = 'Evento'
                    if busca.status_cadastro == 'ativo':
                        resultados = Evento.objects.filter(Q(nome__contains=busca.texto_busca) | Q(local__contains=busca.texto_busca)
                        | Q(endereco__contains=busca.texto_busca) | Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca)
                        | Q(estado__contains=busca.texto_busca)).order_by('dataDeCadastro').reverse().exclude(Q(cadastro_ativo="Não"))
                    else:
                        resultados = Evento.objects.filter(Q(nome__contains=busca.texto_busca) | Q(local__contains=busca.texto_busca)
                        | Q(endereco__contains=busca.texto_busca) | Q(bairro__contains=busca.texto_busca) | Q(cidade__contains=busca.texto_busca)
                        | Q(estado__contains=busca.texto_busca)).order_by('dataDeCadastro').reverse().exclude(Q(cadastro_ativo="Sim"))

                elif busca.tipo_busca == 'produto':
                    classeRetorno = 'Produto'
                    if busca.status_cadastro == 'ativo':
                        resultados = ProdutoDoacao.objects.filter(Q(descricao__contains=busca.texto_busca)).order_by('descricao').exclude(Q(cadastro_ativo="Não"))
                    else:
                        resultados = ProdutoDoacao.objects.filter(Q(descricao__contains=busca.texto_busca)).order_by('descricao').exclude(Q(cadastro_ativo="Sim"))

                elif busca.tipo_busca == 'usuario':
                    classeRetorno = 'Usuario'
                    resultados = User.objects.filter(username__contains=busca.texto_busca)

                elif busca.tipo_busca == 'doacao_entrada':
                    classeRetorno = 'DoacaoEntrada'
                    resultados = DoacaoEntrada.objects.filter(Q(pessoa__nome__contains=busca.texto_busca) | Q(pessoa__cpfCnpj__contains=busca.texto_busca) | Q(produtoDoacao__descricao__contains=busca.texto_busca)).order_by('dataDoacao').reverse()
                    for resultado in resultados:
                        # se existe um produto relacionado à doação do resultado, adiciona na lista
                        if(ProdutoDoadoEntrada.objects.filter(doacaoReferenciaPK=resultado.pk)):
                            # utiliza-se |= para fazer junções de QuerySets
                            produtosDoacao |= ProdutoDoadoEntrada.objects.filter(doacaoReferenciaPK=resultado.pk)

                elif busca.tipo_busca == 'doacao_saida':
                    classeRetorno = 'DoacaoSaida'
                    resultados = DoacaoSaida.objects.filter(Q(pessoa__nome__contains=busca.texto_busca) | Q(pessoa__cpfCnpj__contains=busca.texto_busca) | Q(produtoDoacao__descricao__contains=busca.texto_busca)).order_by('dataDoacao').reverse()
                    for resultado in resultados:
                        # se existe um produto relacionado à doação do resultado, adiciona na lista
                        if(ProdutoDoadoSaida.objects.filter(doacaoReferenciaPK=resultado.pk)):
                            # utiliza-se |= para fazer junções de QuerySets
                            produtosDoacao |= ProdutoDoadoSaida.objects.filter(doacaoReferenciaPK=resultado.pk)

                messages.success(request, 'Consulta realizada com sucesso!', extra_tags='alert alert-success')
                # se não obteve nenhum resultado da busca
                if resultados.count() <= 0:
                    messages.warning(request, 'Nenhum resultado encontrado com este parâmetro.', extra_tags='alert alert-warning')
            else:
                messages.warning(request, 'Erro! Não foi possível efetuar a operação. Tente novamente. Se o problema persistir entre em contato com o suporte.', extra_tags='alert alert-danger')
        else:
            formBusca = BuscaForm()
        return render(request, 'blog/busca.html', {'formBusca': formBusca, 'resultados':resultados, 'busca':busca, 'classeRetorno':classeRetorno, 'produtosDoacao':produtosDoacao})
    except Exception as excecao:
        messages.warning(request, 'Ops, algum erro aconteceu. Verifique os valores digitados e tente novamente. Se o problema persistir, entre com contato com o suporte. Classe: DoacaoEntrada -> except Exception.', extra_tags='alert alert-danger')
        return redirect('busca', pk=1)
