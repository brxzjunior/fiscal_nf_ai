# ia_agente.py

import os
import pandas as pd
from groq import Groq  # SDK oficial da Groq [web:500][web:507]
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Cliente Groq global
groq_client = Groq(api_key=GROQ_API_KEY)


def gerar_resumo_nf(df: pd.DataFrame) -> str:
    """
    Recebe o DataFrame de notas (como o que vai para o Excel)
    e gera um resumo em texto usando Groq (sem Agno por enquanto).
    """
    df_sem_total = df[df["arquivo"] != "TOTAL"]

    resumo_por_emit = (
        df_sem_total
        .groupby("nome_emit")[["total_nf", "icms"]]
        .sum()
        .reset_index()
    )

    contexto = resumo_por_emit.to_string(index=False)

    prompt = f"""
    Você recebeu uma tabela com colunas: nome_emit, total_nf, icms.

    Cada linha representa o total de notas fiscais para um emissor, no período analisado.

    DADOS:
    {contexto}

    Gere um resumo curto, em português, abordando:
    - Faturamento total aproximado.
    - Quem são os principais emissores (maiores valores).
    - Comentário rápido sobre o ICMS (valores mais altos / concentração).

    Não devolva tabela nem código, apenas um texto corrido em 1 a 3 parágrafos.
    """

    chat_completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # modelo da Groq [web:502][web:504]
        messages=[
            {
                "role": "system",
                "content": "Você é um contador sênior que explica resultados de NF-e em português simples.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
    )

    return chat_completion.choices[0].message.content.strip()
