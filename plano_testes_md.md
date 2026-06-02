# 📋 DOCUMENTO DE PLANO DE TESTES (TEST PLAN)

**Projeto:** API de Gerenciamento de Almoxarifado (SAEP)  
**Módulo:** Gestão de Estoque e Movimentações  
**Tipo de Teste:** Teste Funcional e Validação de Regras de Negócio  
**Ambiente:** Desenvolvimento (Localhost)  

---

## 🛠️ DADOS DO AMBIENTE E MASSA DE TESTES

* **Base URL:** `http://127.0.0.1:8000/api/`
* **Ferramenta de API:** Postman / Insomnia
* **Perfis de Usuário:**
  * Administrador: `senai` (Senha: `123`)
  * Operador: `vinicius` (Senha: `senai123`)

---

## 🧪 CASOS DE TESTE (TEST CASES)

### 🛑 CT-01: Validar bloqueio de saída por estoque insuficiente
**Módulo:** Movimentações | **Prioridade:** Alta

* **Descrição:** Garantir que o sistema de back-end faça a trava de segurança e não permita saldo negativo no banco de dados.
* **Pré-condições:** 1. Estar autenticado na API.
  2. Possuir um produto cadastrado (Ex: ID 1 com estoque = 10).
* **Passos para Execução (Steps):**
  1. Enviar requisição `POST` para o endpoint `/movimentacoes/`.
  2. Inserir no Body (JSON) os dados do produto ID 1.
  3. Definir o campo `"tipo": "S"`.
  4. Definir o campo `"quantidade"` com o valor `9999` (maior que o estoque).
* **Resultado Esperado:** A API deve recusar a requisição, não alterar o banco de dados e retornar o status code **400 Bad Request** contendo a mensagem de erro: *"Saída não permitida: estoque insuficiente"*.

---

### ✅ CT-02: Validar fluxo de saída com sucesso (Perfil Administrador)
**Módulo:** Movimentações | **Prioridade:** Alta

* **Descrição:** Verificar se o sistema realiza a dedução correta do saldo de estoque e se rastreia o autor da ação (Admin).
* **Pré-condições:**
  1. Estar autenticado com a credencial de Administrador (`senai`).
  2. Possuir produto com saldo suficiente.
* **Passos para Execução (Steps):**
  1. Enviar requisição `POST` para o endpoint `/movimentacoes/`.
  2. Inserir no Body (JSON) os dados do produto ID 1.
  3. Definir o campo `"tipo": "S"`.
  4. Definir o campo `"quantidade"` com um valor válido (Ex: `5`).
* **Resultado Esperado:** A API deve processar a baixa, atualizar o produto e retornar o status code **201 Created**. O JSON de resposta deve conter o ID/Nome do usuário `senai` e a data/hora atual (Rastreabilidade).

---

### 👤 CT-03: Validar permissão de saída para Operador (Não-Admin)
**Módulo:** Movimentações e Permissões | **Prioridade:** Média

* **Descrição:** Comprovar que contas com privilégios reduzidos (Operador) possuem autorização de escrita para movimentações e que o sistema registra corretamente esse perfil.
* **Pré-condições:**
  1. Estar autenticado com a credencial de Operador (`vinicius`).
  2. Possuir produto com saldo suficiente.
* **Passos para Execução (Steps):**
  1. Enviar requisição `POST` para o endpoint `/movimentacoes/`.
  2. Inserir no Body (JSON) os dados do produto ID 1.
  3. Definir o campo `"tipo": "S"`.
  4. Definir o campo `"quantidade"` com o valor `1`.
* **Resultado Esperado:** O sistema deve reconhecer a permissão do Operador, efetuar a baixa de estoque e retornar **201 Created**. O JSON retornado deve carimbar a movimentação obrigatoriamente com o nome/id do usuário `vinicius`.