from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Produto, Movimentacao
from django.utils import timezone

# Função auxiliar para verificar se o usuário é Administrador
def eh_administrador(user):
    return user.is_superuser or user.groups.filter(name='Administrador').exists()

@login_required
def listar_produtos(request):
    # Regra de negócio: Listagem com filtros por nome e data
    queryset = Produto.objects.all().order_by('nome')
    
    nome_filtro = request.GET.get('nome')
    if nome_filtro:
        queryset = queryset.filter(nome__icontains=nome_filtro)
        
    data_filtro = request.GET.get('data')
    if data_filtro:
        queryset = queryset.filter(data_cadastro__date=data_filtro)

    # Regra de negócio: Paginação (exibindo 10 produtos por página)
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    produtos = paginator.get_page(page_number)
    
    return render(request, 'almoxarifado/listar_produtos.html', {'produtos': produtos})

@login_required
def registrar_movimentacao(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade'))
        
        # Cria a movimentação registrando o usuário logado e a data/hora atual automaticamente
        nova_movimentacao = Movimentacao(
            produto=produto,
            tipo=tipo,
            quantidade=quantidade,
            usuario_responsavel=request.user,
            data_hora=timezone.now()
        )
        
        try:
            nova_movimentacao.save()
            messages.success(request, "Movimentação registrada com sucesso!")
            return redirect('listar_produtos')
        except ValidationError as e:
            
            messages.error(request, e.message)
            
    return render(request, 'almoxarifado/registrar_movimentacao.html', {'produto': produto})

# Funcionalidade exclusiva do Administrador (Concessão direta de privilégios)
@login_required
@user_passes_test(eh_administrador, login_url='listar_produtos')
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    messages.success(request, "Produto excluído com sucesso pelo Administrador.")
    return redirect('listar_produtos')