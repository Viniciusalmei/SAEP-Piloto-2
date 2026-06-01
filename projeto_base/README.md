# Projeto Base - Gerenciamento de Almoxarifado

Este é o projeto base em Django para a realização da prova. O sistema já possui a estrutura básica de modelos, API e autenticação funcionando.

## Configurações Iniciais

- **Superusuário**: `admin` / `admin123`
- **Base URL da API**: `/api/`
- **Autenticação**: `/api-auth/`

## O que deve ser feito (Requisitos do Documento)

1. **Tipos de Usuários**: Implementar lógica para distinguir entre `Operador de Almoxarifado` e `Administrador`.
2. **Controle de Acesso**: 
   - Operador: GET, POST, PUT.
   - Administrador: GET, POST, PUT, DELETE.
3. **Lógica de Estoque**: No momento da criação de uma `Movimentacao` de saída (S):
   - Validar se há estoque disponível.
   - Bloquear se a quantidade solicitada for maior que o saldo.
   - Retornar mensagem: “Saída não permitida: estoque insuficiente. Disponível X: Solicitado: Y”.
   - Se permitido, atualizar o campo `quantidade_estoque` do `Produto`.
4. **Paginação e Filtros**: Já configurados, mas verifique se atendem aos requisitos de filtro por nome e data.
5. **Testes**: Criar a pasta `docs` e o arquivo `plano_testes.docx` conforme as instruções.

## Como rodar

1. Instale as dependências: `pip install django djangorestframework django-filter`
2. Execute as migrações: `python manage.py migrate`
3. Inicie o servidor: `python manage.py runserver`
