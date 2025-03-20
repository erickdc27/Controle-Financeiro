import sqlite3
import os

def conectar_banco():
    caminho = os.path.join('data', 'controle_financeiro.db')
    return sqlite3.connect(caminho)

def criar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY, nome TEXT, percentual_recomendado REAL)''')
    cursor.executemany('INSERT OR IGNORE INTO categorias (id, nome, percentual_recomendado) VALUES (?, ?, ?)', [(1, 'Gastos Essenciais', 50), (2, 'Desejos Pessoais e Lazer', 30), (3, 'Investimentos e Dividas', 20)])
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (id INTEGER PRIMARY KEY, valor REAL, data TEXT, descricao TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas (id INTEGER PRIMARY KEY, valor REAL, data TEXT, descricao TEXT, categoria_id INTEGER, FOREIGN KEY (categoria_id) REFERENCES categorias(id))''')
    conn.commit()
    conn.close()
