# 📦 API Gerenciamento de Almoxarifado

Sistema de back-end desenvolvido em Django REST Framework para controle de estoque e gerenciamento de permissões.

---

## 🔐 Credenciais de Acesso (Testes)

Utilize os usuários abaixo para testar as regras de permissão na API:

- **Administrador (Superusuário)**:
  - Usuário: `senai`
  - Senha: `123`

- **Operador de Almoxarifado**:
  - Usuário: `vinicius`
  - Senha: `senai123`

---

## 🛣️ Rotas da API (Endpoints)

Abaixo estão as rotas disponíveis no sistema para navegação e testes via navegador, Postman ou Insomnia:

* **Login (Autenticação por Sessão):** `http://127.0.0.1:8000/api-auth/login/`
* **Painel Raiz da API (Lista de rotas):** `http://127.0.0.1:8000/api/`

### 📦 Módulo de Produtos
* **URL:** `http://127.0.0.1:8000/api/produtos/`
* **Métodos Suportados:** 
  * `GET`, `POST` (Acesso para Admin e Operador).
  * `PUT`, `DELETE` (Acesso restrito ao Admin).
* **Filtros e Paginação:** Suporta paginação nativa configurada para 5 itens por página e filtros por query params (`?nome=` e `?data_cadastro=`).

### 🔄 Módulo de Movimentações (Controle de Estoque)
* **URL:** `http://127.0.0.1:8000/api/movimentacoes/`
* **Métodos Suportados:** 
  * `GET`, `POST` (Acesso para Admin e Operador).
  * `PUT`, `DELETE` (Acesso restrito ao Admin).
* **Regras de Negócio Automáticas no método POST:** 
  * Deduz ou adiciona ao estoque do Produto automaticamente.
  * Valida e bloqueia operações de saída (`S`) que sejam maiores que o saldo disponível em estoque.
  * Registra de forma automática o usuário logado responsável pela ação.