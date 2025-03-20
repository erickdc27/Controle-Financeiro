from app.banco import conectar_banco
from datetime import datetime
import matplotlib.pyplot as plt

def gerar_graficos(mes_ano):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM receitas WHERE data LIKE ?", (f"{mes_ano}%",))
    total_receitas = cursor.fetchone()[0]

    cursor.execute("""SELECT c.nome, c.percentual_recomendado, COALESCE(SUM(d.valor), 0)
                      FROM categorias c
                      LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ?
                      GROUP BY c.id, c.nome, c.percentual_recomendado""", (f"{mes_ano}%",))
    categorias = cursor.fetchall()

    nomes_categorias = [c[0] for c in categorias]
    gastos_categorias = [c[2] for c in categorias]
    limites_categorias = [(c[1] / 100) * total_receitas for c in categorias]

    # Gráfico de barras comparando limite e gasto por categoria
    x = range(len(nomes_categorias))
    plt.figure(figsize=(10, 6))
    plt.bar(x, limites_categorias, width=0.4, label='Limite (R$)', align='center')
    plt.bar([p + 0.4 for p in x], gastos_categorias, width=0.4, label='Gasto Real (R$)', align='center')
    plt.xticks([p + 0.2 for p in x], nomes_categorias, rotation=45)
    plt.ylabel('Valor (R$)')
    plt.title(f'Comparativo Limite x Gasto - {mes_ano}')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Gráfico de pizza com percentual de gastos
    if sum(gastos_categorias) > 0:
        plt.figure(figsize=(8, 8))
        plt.pie(gastos_categorias, labels=nomes_categorias, autopct='%1.1f%%', startangle=90)
        plt.title(f'Distribuição de Gastos por Categoria - {mes_ano}')
        plt.show()

    conn.close()
