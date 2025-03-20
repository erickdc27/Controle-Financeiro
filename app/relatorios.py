from app.banco import conectar_banco
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def exportar_relatorio_pdf(mes_ano):
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM receitas WHERE data LIKE ?", (f"{mes_ano}%",))
    total_receitas = cursor.fetchone()[0]

    cursor.execute("""SELECT c.nome, c.percentual_recomendado, COALESCE(SUM(d.valor), 0)
                      FROM categorias c
                      LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ?
                      GROUP BY c.id, c.nome, c.percentual_recomendado""", (f"{mes_ano}%",))
    categorias = cursor.fetchall()

    nome_arquivo = f"relatorio_financeiro_{mes_ano.replace('-', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, f"Relatório Financeiro - {mes_ano}")

    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 80, f"Receita Total: R$ {total_receitas:.2f}")

    y_pos = altura - 120
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Categoria")
    c.drawString(200, y_pos, "Limite (%)")
    c.drawString(300, y_pos, "Gasto (R$)")
    c.drawString(400, y_pos, "Utilizado (%)")
    c.drawString(500, y_pos, "Status")

    c.setFont("Helvetica", 10)
    y_pos -= 20

    for nome, limite, gasto in categorias:
        percentual_utilizado = (gasto / total_receitas * 100) if total_receitas > 0 else 0
        status = "OK" if (limite/100 * total_receitas) >= gasto else "Excedido"

        c.drawString(50, y_pos, nome)
        c.drawString(200, y_pos, f"{limite:.0f}%")
        c.drawString(300, y_pos, f"R$ {gasto:.2f}")
        c.drawString(400, y_pos, f"{percentual_utilizado:.1f}%")
        c.drawString(500, y_pos, status)

        y_pos -= 20
        if y_pos < 50:
            c.showPage()
            y_pos = altura - 50

    c.save()
    conn.close()

    print(f"Relatório exportado com sucesso: {nome_arquivo}")
