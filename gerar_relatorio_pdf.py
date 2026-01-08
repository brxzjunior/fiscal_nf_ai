import pandas as pd   # Importa o pandas para ler o Excel com os dados das NFs

# Importa objetos básicos do ReportLab para gerar PDF
from reportlab.lib.pagesizes import A4  # tamanho da página A4 [web:586]
from reportlab.pdfgen import canvas    # "tela" onde vamos desenhar o PDF [web:584]


def gerar_relatorio_pdf(caminho_excel: str) -> str:
    """
    Gera um PDF simples a partir de um arquivo Excel já existente
    e retorna o caminho do PDF gerado.
    """

    # Lê o Excel com os dados das notas
    # Aqui supõe que seu Excel já tem colunas como 'emitente', 'total_nf' e 'icms'
    df = pd.read_excel(caminho_excel)

    # Define o nome do PDF com base no nome do Excel
    caminho_pdf = caminho_excel.replace(".xlsx", ".pdf")

    # Cria o canvas (folha em branco) do PDF em tamanho A4
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    width, height = A4  # largura e altura da página

    # Título do relatório
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de NF-e - Fiscal IA Pro")

    # Subtítulo com alguma info básica (opcional)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Fonte: {caminho_excel}")

    # Posição inicial do texto da tabela
    y = height - 100

    # Cabeçalho das colunas no PDF
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Emitente")
    c.drawString(250, y, "Total NF")
    c.drawString(350, y, "ICMS")
    y -= 18

    # Volta para fonte normal para as linhas
    c.setFont("Helvetica", 10)

    # Itera nas primeiras linhas do DataFrame para não lotar a página
    # Ajuste o .head(30) conforme a quantidade típica de dados.
    for _, row in df.head(30).iterrows():
        emitente = str(row.get("emitente", ""))[:25]  # corta para não extrapolar
        total_nf = str(row.get("total_nf", ""))
        icms = str(row.get("icms", ""))

        c.drawString(50, y, emitente)
        c.drawString(250, y, total_nf)
        c.drawString(350, y, icms)

        y -= 14

        # Se chegar muito perto do rodapé, cria nova página
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    # Finaliza o PDF
    c.showPage()
    c.save()

    # Retorna o caminho do arquivo PDF gerado
    return caminho_pdf
