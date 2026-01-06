import pandas as pd                                      # Biblioteca para manipulação de dados
import time                                              # Para gerar timestamps
import xmltodict                                         # Para converter XML em dicionário Python
from fastapi import FastAPI, UploadFile, File, HTTPException  # FastAPI núcleo + tipos de upload + exceções HTTP
from fastapi.middleware.cors import CORSMiddleware       # Middleware para CORS
from fastapi.responses import FileResponse               # Para devolver arquivos
from fastapi.responses import HTMLResponse               # Para devolver HTML
from typing import List         
from ia_agente import gerar_resumo_nf
                         # Tipagem de lista para múltiplos arquivos


def extrair_inf_nfe(data: dict) -> dict:
    """
    Aceita tanto:
    - nfeProc -> NFe -> infNFe
    - NFe -> infNFe
    Retorna sempre o dict de infNFe.
    """
    if "nfeProc" in data:
        return data["nfeProc"]["NFe"]["infNFe"]
    if "NFe" in data:
        return data["NFe"]["infNFe"]
    for k in data.keys():
        if k.endswith("NFe"):
            return data[k]["infNFe"]
    raise KeyError("Estrutura de NF-e não reconhecida")


app = FastAPI(title="FiscalIA Pro")
# Cria a aplicação FastAPI com um título para o Swagger (/docs)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Libera acesso de qualquer origem (bom para teste)
    allow_methods=["*"],    # Libera todos os métodos HTTP
    allow_headers=["*"]     # Libera todos os headers
)


@app.get("/health")
async def health():
    # Endpoint simples para checar se a API está ON
    return {"status": "🚀 FiscalIA Pro rodando!", "ok": True}


@app.post("/processar-xml")
async def processar_xml(file: UploadFile = File(...)):
    """Upload 1 XML → extrai CNPJ/total"""
    try:
        content = await file.read()          # Lê o conteúdo do arquivo (bytes)
        data = xmltodict.parse(content)      # Converte XML em dict

        # DEBUG: para ver no terminal a estrutura do XML
        print("RAIZ KEYS:", list(data.keys()))

        nfe = extrair_inf_nfe(data)          # Navega até o bloco principal da NF-e

        return {
            "cnpj_emit": nfe["emit"]["CNPJ"],
            "nome_emit": nfe["emit"]["xNome"],
            "total_nf": float(nfe["total"]["ICMSTot"]["vNF"]),
            "icms": float(nfe["total"]["ICMSTot"]["vICMS"]),
        }
    except Exception as e:
        # Se der qualquer erro (KeyError, parse, etc.), loga e retorna 500 para o cliente
        print("ERRO AO PROCESSAR XML:", repr(e))
        raise HTTPException(status_code=500, detail=f"Erro ao processar XML: {e}")


@app.post("/processar-nfes")
async def processar_nfes(files: List[UploadFile] = File(...)):
    """
    Recebe vários XMLs, extrai dados, soma totais
    e gera um relatório Excel mais amigável.
    """
    resultados = []          # Lista com os dados de cada nota
    total_geral = 0.0        # Soma de vNF (valor total das notas)
    total_icms = 0.0         # Soma de ICMS

    for file in files:       # Loop em cada arquivo enviado
        try:
            content = await file.read()      # Lê bytes do XML
            data = xmltodict.parse(content)  # Converte XML em dict
            nfe = extrair_inf_nfe(data)

            valor_nf = float(nfe["total"]["ICMSTot"]["vNF"])      # Valor total desta NF
            valor_icms = float(nfe["total"]["ICMSTot"]["vICMS"])  # ICMS desta NF

            total_geral += valor_nf          # Acumula no total geral
            total_icms += valor_icms         # Acumula ICMS total

            resultados.append({
                "arquivo": file.filename,
                "cnpj_emit": nfe["emit"]["CNPJ"],
                "nome_emit": nfe["emit"]["xNome"],
                "total_nf": valor_nf,
                "icms": valor_icms,
            })
        except Exception as e:
            # Se alguma NF der erro, loga qual arquivo quebrou
            print(f"ERRO NO ARQUIVO {file.filename}:", repr(e))
            # Aqui vou só lançar um erro geral:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar XML {file.filename}: {e}"
            )

    # Geração do Excel melhorado (fora do loop)
    df = pd.DataFrame(resultados)

    # Ordena por nome do emitente e depois por valor (do maior para o menor)
    df = df.sort_values(by=["nome_emit", "total_nf"], ascending=[True, False])

    # Adiciona linha de TOTAL ao final da planilha
    linha_total = {
        "arquivo": "TOTAL",
        "cnpj_emit": "",
        "nome_emit": "",
        "total_nf": total_geral,
        "icms": total_icms,
    }

    # Adiciona a linha total ao DataFrame
    df = pd.concat([df, pd.DataFrame([linha_total])], ignore_index=True)

    # Nome único para o arquivo (evita sobrescrever)
    nome_arquivo = f"relatorio_nfes_{int(time.time())}.xlsx"

    # Usa ExcelWriter com openpyxl para poder formatar
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Relatorio")

        workbook = writer.book
        worksheet = writer.sheets["Relatorio"]

        # Descobre última linha (linha TOTAL) em 1-based (cabeçalho é linha 1)
        last_row = df.shape[0] + 1

        from openpyxl.styles import Font

        # Formatação de moeda nas colunas de valor (total_nf e icms)
        # Supondo colunas:
        # A: arquivo, B: cnpj_emit, C: nome_emit, D: total_nf, E: icms
        for row in range(2, last_row + 1):  # da primeira linha de dados até TOTAL
            worksheet[f"D{row}"].number_format = "#,##0.00"
            worksheet[f"E{row}"].number_format = "#,##0.00"

        # Deixa a linha TOTAL em negrito
        bold_font = Font(b=True)
        for col in range(1, 6):   # colunas A até E
            cell = worksheet.cell(row=last_row, column=col)
            cell.font = bold_font

    # Retorna quantidade de notas, soma dos valores e lista individual
    return {
        "qtd": len(resultados),
        "total_geral": total_geral,
        "total_icms": total_icms,
        "relatorio_excel": nome_arquivo,
        "notas": resultados,
    }


@app.get("/download-relatorio")
async def download_relatorio(nome_arquivo: str):
    """
    Faz o download do arquivo Excel gerado.
    Use o nome retornado em 'relatorio_excel'.
    """
    try:
        return FileResponse(
            path=nome_arquivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=nome_arquivo,
            headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"}
        )
    except Exception as e:
        print("ERRO AO ENVIAR EXCEL:", repr(e))
        raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {nome_arquivo}")


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <meta charset="utf-8" />
        <title>FiscalIA Pro</title>
      </head>
      <body>
        <h1>FiscalIA Pro - Relatório de NF-e</h1>
        <p>Selecione os XMLs e clique em "Gerar relatório".</p>

        <form id="form-nfes" enctype="multipart/form-data">
          <input name="files" type="file" multiple />
          <button type="button" onclick="enviar()">Gerar relatório</button>
        </form>

        <div id="resultado" style="margin-top: 16px;"></div>
        <div id="resumo-ia" style="margin-top: 16px; white-space: pre-wrap;"></div>

        <script>
        async function enviar() {
          const form = document.getElementById('form-nfes');
          const formData = new FormData(form);

          const resp = await fetch('/processar-nfes', {
            method: 'POST',
            body: formData
          });

          const data = await resp.json();

          if (resp.ok) {
            const div = document.getElementById('resultado');
            div.innerHTML =
              'Notas: ' + data.qtd +
              ' | Total: ' + data.total_geral.toFixed(2) +
              ' | ICMS: ' + data.total_icms.toFixed(2) +
              '<br><a href="/download-relatorio?nome_arquivo=' + data.relatorio_excel + '">Baixar Excel</a>' +
              '<br><button type="button" onclick="gerarResumoIA(\\'' + data.relatorio_excel + '\\')">Gerar resumo IA</button>';
          } else {
            alert('Erro: ' + (data.detail || 'erro ao processar'));
          }
        }

        async function gerarResumoIA(nomeArquivo) {
          const resp = await fetch('/resumo-ia?nome_arquivo=' + encodeURIComponent(nomeArquivo));
          const data = await resp.json();

          if (resp.ok) {
            document.getElementById('resumo-ia').innerText = data.resumo;
          } else {
            alert('Erro IA: ' + (data.detail || 'erro ao gerar resumo'));
          }
        }
        </script>
      </body>
    </html>
    """


@app.get("/resumo-ia")
async def resumo_ia(nome_arquivo: str):
    df = pd.read_excel(nome_arquivo)
    texto = gerar_resumo_nf(df)
    return {"resumo": texto}


if __name__ == "__main__":
    import uvicorn
    # Roda a API em http://127.0.0.1:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
