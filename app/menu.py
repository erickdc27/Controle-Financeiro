from app.cadastro import cadastrar_receita, cadastrar_despesa
from app.relatorios import exportar_relatorio_pdf
from app.graficos import gerar_graficos
from app.banco import criar_banco

def menu():
    criar_banco()
    while True:
        print('1 - Cadastrar Receita')
        print('2 - Cadastrar Despesa')
        print('3 - Exportar Relatorio PDF')
        print('4 - Gerar Graficos')
        print('5 - Sair')
        escolha = input('Escolha: ')
        if escolha == '1':
            valor = float(input('Valor: '))
            data = input('Data (YYYY-MM-DD): ')
            desc = input('Descricao: ')
            cadastrar_receita(valor, data, desc)
        elif escolha == '2':
            valor = float(input('Valor: '))
            data = input('Data (YYYY-MM-DD): ')
            print('1 - Gastos Essenciais, 2 - Desejos Pessoais e Lazer, 3 - Investimentos e Dividas')
            cat = int(input('Categoria: '))
            desc = input('Descricao: ')
            cadastrar_despesa(valor, data, cat, desc)
        elif escolha == '3':
            mes_ano = input('Digite o mes/ano (YYYY-MM): ')
            exportar_relatorio_pdf(mes_ano)
        elif escolha == '4':
            mes_ano = input('Digite o mes/ano (YYYY-MM): ')
            gerar_graficos(mes_ano)
        elif escolha == '5':
            break
        else:
            print('Opcao invalida.')
