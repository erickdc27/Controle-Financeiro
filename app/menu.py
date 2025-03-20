from app.cadastro import (
    cadastrar_receita, cadastrar_despesa,
    listar_receitas_por_mes, listar_despesas_por_mes,
    editar_receita, editar_despesa,
    excluir_receita, excluir_despesa
)
from app.relatorios import exportar_relatorio_pdf
from app.graficos import gerar_graficos
from app.banco import criar_banco, conectar_banco
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tabulate import tabulate
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_saldo_por_categoria(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.today().strftime('%Y-%m')

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM receitas WHERE data LIKE ?", (f"{mes_ano}%",))
    total_receitas = cursor.fetchone()[0]

    cursor.execute("""SELECT c.nome, c.percentual_recomendado, COALESCE(SUM(d.valor), 0)
                      FROM categorias c
                      LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ?
                      GROUP BY c.id, c.nome, c.percentual_recomendado""", (f"{mes_ano}%",))
    categorias = cursor.fetchall()

    print(f"\nResumo financeiro do mês {mes_ano}:")
    print(f"Receita total: R$ {total_receitas:.2f}\n")

    tabela = []
    for nome, limite, gasto in categorias:
        percentual_utilizado = (gasto / total_receitas * 100) if total_receitas > 0 else 0
        saldo_categoria = (limite/100 * total_receitas) - gasto
        status = "OK" if saldo_categoria >= 0 else "Excedido"

        tabela.append([
            nome,
            f"Limite: {limite}%",
            f"Gasto: R$ {gasto:.2f}",
            f"Utilizado: {percentual_utilizado:.2f}%",
            f"Saldo: R$ {saldo_categoria:.2f}",
            status
        ])

    print(tabulate(tabela, headers=["Categoria", "Limite", "Gasto", "Utilizado", "Saldo", "Status"], tablefmt="grid"))
    conn.close()

def solicitar_valor():
    while True:
        valor_str = input("Informe o valor (use ponto para decimais): ").replace(',', '.').strip()
        try:
            valor = float(valor_str)
            if valor > 0:
                return valor
            else:
                print("O valor deve ser positivo.")
        except ValueError:
            print("Valor inválido. Digite um número.")

def solicitar_data():
    while True:
        data_input = input("Data (dd/mm/aaaa): ").strip()
        try:
            datetime.strptime(data_input, '%d/%m/%Y')
            return data_input
        except ValueError:
            print("Formato de data inválido. Use dd/mm/aaaa.")

def solicitar_id_existente(cursor, tabela):
    while True:
        id_input = input(f"Informe o ID existente na tabela {tabela}: ").strip()
        if id_input.isdigit():
            cursor.execute(f"SELECT id FROM {tabela} WHERE id = ?", (id_input,))
            if cursor.fetchone():
                return int(id_input)
            else:
                print("ID não encontrado. Tente novamente.")
        else:
            print("Entrada inválida. Digite um número.")

def solicitar_categoria(cursor):
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    print("Categorias disponíveis:")
    for c in categorias:
        print(f"{c[0]} - {c[1]}")
    return solicitar_id_existente(cursor, 'categorias')

def menu():
    criar_banco()
    clear_console()
    mes_atual = datetime.today().strftime('%Y-%m')
    mes_anterior = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m')
    mes_proximo = (datetime.today() + relativedelta(months=1)).strftime('%Y-%m')

    listar_receitas_por_mes(mes_atual)
    listar_despesas_por_mes(mes_atual)
    exibir_saldo_por_categoria(mes_atual)

    while True:
        print("\n====== MENU PRINCIPAL ======")
        print("1 - Criar Receita")
        print("2 - Criar Despesa")
        print("3 - Editar Receita")
        print("4 - Editar Despesa")
        print("5 - Excluir Receita")
        print("6 - Excluir Despesa")
        print("7 - Listar mês atual novamente")
        print("8 - Gerar Relatório PDF do mês atual")
        print("9 - Exibir Gráficos do mês atual")
        print("10 - Listar mês anterior")
        print("11 - Listar próximo mês")
        print("12 - Gerar Relatório PDF do mês anterior")
        print("13 - Gerar Relatório PDF do próximo mês")
        print("14 - Exibir Gráficos do mês anterior")
        print("15 - Exibir Gráficos do próximo mês")
        print("16 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            clear_console()
            valor = solicitar_valor()
            data = solicitar_data()
            descricao = input("Descrição: ")
            cadastrar_receita(valor, data, descricao)

        elif escolha == '2':
            clear_console()
            valor = solicitar_valor()
            data = solicitar_data()
            conn = conectar_banco()
            cursor = conn.cursor()
            categoria_id = solicitar_categoria(cursor)
            descricao = input("Descrição: ")
            cadastrar_despesa(valor, data, categoria_id, descricao)
            conn.close()

        elif escolha == '3':
            clear_console()
            editar_receita()

        elif escolha == '4':
            clear_console()
            editar_despesa()

        elif escolha == '5':
            clear_console()
            excluir_receita()

        elif escolha == '6':
            clear_console()
            excluir_despesa()

        elif escolha == '7':
            clear_console()
            listar_receitas_por_mes(mes_atual)
            listar_despesas_por_mes(mes_atual)
            exibir_saldo_por_categoria(mes_atual)

        elif escolha == '8':
            clear_console()
            exportar_relatorio_pdf(mes_atual)

        elif escolha == '9':
            clear_console()
            gerar_graficos(mes_atual)

        elif escolha == '10':
            clear_console()
            listar_receitas_por_mes(mes_anterior)
            listar_despesas_por_mes(mes_anterior)
            exibir_saldo_por_categoria(mes_anterior)

        elif escolha == '11':
            clear_console()
            listar_receitas_por_mes(mes_proximo)
            listar_despesas_por_mes(mes_proximo)
            exibir_saldo_por_categoria(mes_proximo)

        elif escolha == '12':
            clear_console()
            exportar_relatorio_pdf(mes_anterior)

        elif escolha == '13':
            clear_console()
            exportar_relatorio_pdf(mes_proximo)

        elif escolha == '14':
            clear_console()
            gerar_graficos(mes_anterior)

        elif escolha == '15':
            clear_console()
            gerar_graficos(mes_proximo)

        elif escolha == '16':
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")
