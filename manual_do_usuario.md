# Manual do Usuário — Sistema de Controle Financeiro

## ✅ **Descrição geral:**
Este sistema foi desenvolvido para auxiliar o controle financeiro pessoal e profissional, utilizando a regra 50/30/20 (50% para gastos essenciais, 30% para desejos pessoais e lazer, 20% para investimentos e dívidas). O sistema permite o registro, listagem, edição, exclusão, geração de relatórios e análise gráfica das finanças mensais.

---

## ✅ **Funcionamento ao iniciar:**
Ao abrir o sistema (executando `main.py`), você verá automaticamente:
- Listagem de todas as receitas cadastradas no mês atual.
- Listagem de todas as despesas cadastradas no mês atual.
- Exibição do saldo total, dividido por categoria, indicando se cada limite foi respeitado ou excedido.

---

## ✅ **Menu principal:**
Após a exibição inicial, o sistema apresentará o menu com as seguintes opções:

### 1. **Criar Receita**
- Permite cadastrar uma nova receita.
- Campos solicitados: valor, data (no formato YYYY-MM-DD) e descrição opcional.

### 2. **Criar Despesa**
- Permite cadastrar uma nova despesa.
- Campos solicitados: valor, data, escolha da categoria e descrição.

### 3. **Editar Receita**
- Solicita o ID da receita a ser editada.
- Exibe os dados atuais e permite alterar valor, data e descrição.

### 4. **Editar Despesa**
- Solicita o ID da despesa a ser editada.
- Exibe os dados atuais e permite alterar valor, data, descrição e categoria.

### 5. **Excluir Receita**
- Solicita o ID da receita a ser excluída.
- Exibe os detalhes e pede confirmação antes da exclusão.

### 6. **Excluir Despesa**
- Solicita o ID da despesa a ser excluída.
- Exibe os detalhes e pede confirmação antes da exclusão.

### 7. **Listar novamente receitas, despesas e saldo**
- Atualiza a tela e exibe novamente a visão consolidada do mês atual.

### 8. **Sair**
- Encerra o sistema de forma segura.

---

## ✅ **Alertas automáticos:**
- O sistema avisa sempre que uma categoria exceder o percentual recomendado.
- O saldo por categoria é exibido, mostrando se há sobra ou excesso.

---

## ✅ **Recomendações:**
- Mantenha o ambiente virtual ativado.
- Faça backups periódicos do banco de dados na pasta `data/`.
- Gere relatórios PDF através do módulo apropriado se desejar ter uma versão exportável.

Se precisar de ajuda futura, consulte este manual ou entre em contato com o desenvolvedor responsável pela mentoria do projeto.
