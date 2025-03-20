from app.banco import conectar_banco
from datetime import datetime
from tabulate import tabulate

def cadastrar_receita(valor, data, descricao=None):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO receitas (valor, data, descricao) VALUES (?, ?, ?)', (valor, data, descricao))
    conn.commit()
    conn.close()
    print('Receita cadastrada com sucesso.')

def cadastrar_despesa(valor, data, categoria_id, descricao=None):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO despesas (valor, data, descricao, categoria_id) VALUES (?, ?, ?, ?)', (valor, data, descricao, categoria_id))
    conn.commit()
    conn.close()
    print('Despesa cadastrada com sucesso.')

def listar_receitas_mes_atual():
    mes_atual = datetime.today().strftime('%Y-%m')
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, valor, data, descricao FROM receitas WHERE data LIKE ?", (f"{mes_atual}%",))
    receitas = cursor.fetchall()
    if receitas:
        print("\nReceitas do mês atual:")
        print(tabulate(receitas, headers=['ID', 'Valor (R$)', 'Data', 'Descrição'], tablefmt='grid'))
    else:
        print("\nNenhuma receita cadastrada para o mês atual.")
    conn.close()

def listar_despesas_mes_atual():
    mes_atual = datetime.today().strftime('%Y-%m')
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""SELECT d.id, d.valor, d.data, d.descricao, c.nome AS categoria
                      FROM despesas d
                      JOIN categorias c ON d.categoria_id = c.id
                      WHERE d.data LIKE ?""", (f"{mes_atual}%",))
    despesas = cursor.fetchall()
    if despesas:
        print("\nDespesas do mês atual:")
        print(tabulate(despesas, headers=['ID', 'Valor (R$)', 'Data', 'Descrição', 'Categoria'], tablefmt='grid'))
    else:
        print("\nNenhuma despesa cadastrada para o mês atual.")
    conn.close()

def editar_receita():
    conn = conectar_banco()
    cursor = conn.cursor()
    receita_id = input("\nInforme o ID da receita que deseja editar: ")
    cursor.execute("SELECT id, valor, data, descricao FROM receitas WHERE id = ?", (receita_id,))
    receita = cursor.fetchone()
    if receita:
        print(f"\nReceita atual: ID: {receita[0]} | Valor: R$ {receita[1]:.2f} | Data: {receita[2]} | Descrição: {receita[3]}")
        novo_valor = input("Novo valor (ou ENTER para manter o atual): ")
        nova_data = input("Nova data (YYYY-MM-DD) (ou ENTER para manter): ")
        nova_descricao = input("Nova descrição (ou ENTER para manter): ")
        valor_final = float(novo_valor) if novo_valor else receita[1]
        data_final = nova_data if nova_data else receita[2]
        descricao_final = nova_descricao if nova_descricao else receita[3]
        cursor.execute("UPDATE receitas SET valor = ?, data = ?, descricao = ? WHERE id = ?",
                       (valor_final, data_final, descricao_final, receita_id))
        conn.commit()
        print("Receita atualizada com sucesso.")
    else:
        print("Receita não encontrada.")
    conn.close()

def editar_despesa():
    conn = conectar_banco()
    cursor = conn.cursor()
    despesa_id = input("\nInforme o ID da despesa que deseja editar: ")
    cursor.execute("""SELECT d.id, d.valor, d.data, d.descricao, c.nome
                      FROM despesas d
                      JOIN categorias c ON d.categoria_id = c.id
                      WHERE d.id = ?""", (despesa_id,))
    despesa = cursor.fetchone()
    if despesa:
        print(f"\nDespesa atual: ID: {despesa[0]} | Valor: R$ {despesa[1]:.2f} | Data: {despesa[2]} | Descrição: {despesa[3]} | Categoria: {despesa[4]}")
        novo_valor = input("Novo valor (ou ENTER para manter): ")
        nova_data = input("Nova data (YYYY-MM-DD) (ou ENTER para manter): ")
        nova_descricao = input("Nova descrição (ou ENTER para manter): ")
        cursor.execute("SELECT id, nome FROM categorias")
        categorias = cursor.fetchall()
        print("\nCategorias disponíveis:")
        for c in categorias:
            print(f"{c[0]} - {c[1]}")
        nova_categoria = input("Nova categoria (ID) (ou ENTER para manter): ")
        valor_final = float(novo_valor) if novo_valor else despesa[1]
        data_final = nova_data if nova_data else despesa[2]
        descricao_final = nova_descricao if nova_descricao else despesa[3]
        if not nova_categoria:
            cursor.execute("SELECT categoria_id FROM despesas WHERE id = ?", (despesa_id,))
            categoria_final = cursor.fetchone()[0]
        else:
            categoria_final = int(nova_categoria)
        cursor.execute("UPDATE despesas SET valor = ?, data = ?, descricao = ?, categoria_id = ? WHERE id = ?",
                       (valor_final, data_final, descricao_final, categoria_final, despesa_id))
        conn.commit()
        print("Despesa atualizada com sucesso.")
    else:
        print("Despesa não encontrada.")
    conn.close()

def excluir_receita():
    conn = conectar_banco()
    cursor = conn.cursor()
    receita_id = input("\nInforme o ID da receita que deseja excluir: ")
    cursor.execute("SELECT id, valor, data, descricao FROM receitas WHERE id = ?", (receita_id,))
    receita = cursor.fetchone()
    if receita:
        print(f"\nReceita encontrada: ID: {receita[0]} | Valor: R$ {receita[1]:.2f} | Data: {receita[2]} | Descrição: {receita[3]}")
        confirmacao = input("Tem certeza que deseja excluir esta receita? (S/N): ").strip().upper()
        if confirmacao == 'S':
            cursor.execute("DELETE FROM receitas WHERE id = ?", (receita_id,))
            conn.commit()
            print("Receita excluída com sucesso.")
        else:
            print("Exclusão cancelada.")
    else:
        print("Receita não encontrada.")
    conn.close()

def excluir_despesa():
    conn = conectar_banco()
    cursor = conn.cursor()
    despesa_id = input("\nInforme o ID da despesa que deseja excluir: ")
    cursor.execute("""SELECT d.id, d.valor, d.data, d.descricao, c.nome
                      FROM despesas d
                      JOIN categorias c ON d.categoria_id = c.id
                      WHERE d.id = ?""", (despesa_id,))
    despesa = cursor.fetchone()
    if despesa:
        print(f"\nDespesa encontrada: ID: {despesa[0]} | Valor: R$ {despesa[1]:.2f} | Data: {despesa[2]} | Descrição: {despesa[3]} | Categoria: {despesa[4]}")
        confirmacao = input("Tem certeza que deseja excluir esta despesa? (S/N): ").strip().upper()
        if confirmacao == 'S':
            cursor.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
            conn.commit()
            print("Despesa excluída com sucesso.")
        else:
            print("Exclusão cancelada.")
    else:
        print("Despesa não encontrada.")
    conn.close()
