from app.banco import conectar_banco

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
