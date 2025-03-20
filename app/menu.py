from app.cadastro import (
    cadastrar_receita, cadastrar_despesa,
    listar_receitas_mes_atual, listar_despesas_mes_atual,
    editar_receita, editar_despesa,
    excluir_receita, excluir_despesa
)
from app.banco import criar_banco, conectar_banco
from datetime import datetime
from tabulate import tabulate

def exibir_saldo_por_categoria():
    mes_atual = datetime.today().strftime('%Y-%m')
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM receitas WHERE data LIKE ?", (f"{mes_atual}%",))
    total_receitas = cursor.fetchone()[0]

    cursor.execute("""SELECT c.nome, c.percentual_recomendado, COALESCE(SUM(d.valor), 0)
                      FROM categorias c
                      LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ?
                      GROUP BY c.id, c.nome, c.percentual_recomendado""", (f"{mes_atual}%",))
    categorias = cursor.fetchall()

    print(f"\nResumo financeiro do mês atual ({mes_atual}):")
    print(f"Receita total: R$ {total_receitas:.2f}\n")

    tabela = []
    for nome, limite, gasto in categorias:
        percentual_utilizado = (gasto / total_receitas * 100) if total_receitas > 0 else 0
        saldo_categoria = (limite/100 * total_receitas) - gasto
        status = "OK"
        if saldo_categoria < 0:
            status = "Excedido"

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

def menu():
    criar_banco()
    listar_receitas_mes_atual()
    listar_despesas_mes_atual()
    exibir_saldo_por_categoria()

    while True:
        print("\n====== MENU PRINCIPAL ======")
        print("1 - Criar Receita")
        print("2 - Criar Despesa")
        print("3 - Editar Receita")
        print("4 - Editar Despesa")
        print("5 - Excluir Receita")
        print("6 - Excluir Despesa")
        print("7 - Listar receitas, despesas e saldo novamente")
        print("8 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            valor = float(input("Valor da receita: "))
            data = input("Data (YYYY-MM-DD): ")
            descricao = input("Descrição: ")
            cadastrar_receita(valor, data, descricao)

        elif escolha == '2':
            valor = float(input("Valor da despesa: "))
            data = input("Data (YYYY-MM-DD): ")
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM categorias")
            categorias = cursor.fetchall()
            for c in categorias:
                print(f"{c[0]} - {c[1]}")
            categoria_id = int(input("Informe o ID da categoria: "))
            descricao = input("Descrição: ")
            cadastrar_despesa(valor, data, categoria_id, descricao)
            conn.close()

        elif escolha == '3':
            editar_receita()

        elif escolha == '4':
            editar_despesa()

        elif escolha == '5':
            excluir_receita()

        elif escolha == '6':
            excluir_despesa()

        elif escolha == '7':
            listar_receitas_mes_atual()
            listar_despesas_mes_atual()
            exibir_saldo_por_categoria()

        elif escolha == '8':
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")
