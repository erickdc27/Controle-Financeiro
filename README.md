# Sistema de Controle Financeiro

Este projeto foi desenvolvido em Python para auxiliar no controle financeiro pessoal, baseado na regra 50/30/20.

## Funcionalidades:
- Cadastro de receitas e despesas
- Relatórios mensais
- Exportação para PDF
- Gráficos visuais de análise financeira

## Estrutura:
- `app/` : Contém os módulos do sistema  
- `data/` : Banco de dados gerado  
- `reports/` : Relatórios PDF gerados  
- `tests/` : Testes automatizados  

## Como executar o projeto

### 1. Criação e ativação do ambiente virtual
- No terminal, na raiz do projeto:
```bash
python -m venv venv
```

- Ative o ambiente:
  - No Windows:
```bash
venv\Scripts\activate
```
  - No Linux/Mac:
```bash
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o projeto
```bash
python main.py
```

### 4. Desativar o ambiente virtual (quando finalizar)
```bash
deactivate
```

## Observação
Certifique-se de manter o ambiente virtual ativo sempre que for rodar o projeto ou instalar novas dependências.
