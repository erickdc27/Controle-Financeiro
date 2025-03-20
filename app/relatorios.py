from app.banco import conectar_banco
from reportlab.pdfgen import canvas
import os

def exportar_relatorio_pdf(mes_ano):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(valor) FROM receitas WHERE data LIKE ?', (f'{mes_ano}%',))
    total_receitas = cursor.fetchone()[0] or 0
    cursor.execute('''SELECT c.nome, c.percentual_recomendado, COALESCE(SUM(d.valor), 0) FROM categorias c LEFT JOIN despesas d ON c.id = d.categoria_id AND d.data LIKE ? GROUP BY c.id''', (f'{mes_ano}%',))
    resultados = cursor.fetchall()
    if not os.path.exists('reports'):
        os.makedirs('reports')
    caminho_pdf = f'reports/Relatorio_{mes_ano}.pdf'
    pdf = canvas.Canvas(caminho_pdf)
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(50, 800, f'Relatorio {mes_ano}')
    y = 770
    for nome, limite, valor in resultados:
        percentual = (valor / total_receitas * 100) if total_receitas > 0 else 0
        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, y, f'{nome}: {percentual:.2f}% usado, limite {limite}%. Valor: R$ {valor:.2f}')
        y -= 20
    pdf.save()
    conn.close()
    print(f'Relatorio PDF exportado em {caminho_pdf}')
