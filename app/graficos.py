import matplotlib.pyplot as plt
from app.banco import conectar_banco

def gerar_graficos(mes_ano):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''SELECT c.nome, COALESCE(SUM(d.valor), 0) FROM categorias c LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ? GROUP BY c.id''', (f'{mes_ano}%',))
    dados = cursor.fetchall()
    nomes = [linha[0] for linha in dados]
    valores = [linha[1] for linha in dados]
    plt.figure(figsize=(8, 6))
    plt.pie(valores, labels=nomes, autopct='%1.1f%%')
    plt.title(f'Distribuicao de despesas - {mes_ano}')
    plt.show()
    conn.close()
