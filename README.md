# FiscalIA Pro

FiscalIA Pro é uma ferramenta para processar lotes de arquivos XML de Notas Fiscais eletrônicas (NF-e). A aplicação extrai informações importantes de cada nota, compila os dados em um relatório Excel e, opcionalmente, gera um resumo analítico usando inteligência artificial.

## Funcionalidades

- **Upload de Múltiplos XMLs**: Envie um ou vários arquivos XML de NF-e de uma só vez.
- **Extração de Dados**: Extrai informações como CNPJ do emitente, nome, valor total da nota e valor do ICMS.
- **Relatório em Excel**: Gera um arquivo `.xlsx` com os dados organizados, incluindo uma linha de totais e formatação de moeda.
- **Resumo com IA**: Utiliza a API da Groq para gerar um resumo em linguagem natural sobre os dados processados, destacando os principais emissores e o impacto do ICMS.
- **Interface Simples**: Uma página web simples para upload dos arquivos e visualização dos resultados.

## Tecnologias Utilizadas

- **Back-end**: Python, FastAPI
- **Processamento de Dados**: Pandas
- **Inteligência Artificial**: Groq SDK
- **Servidor**: Uvicorn

## Pré-requisitos

- Python 3.10.0

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd fiscal_ai_pro
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Windows
    python -m venv fiscalia_env
    .\fiscalia_env\Scripts\activate

    # macOS/Linux
    python3 -m venv fiscalia_env
    source fiscalia_env/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

1.  **Crie um arquivo `.env`:**
    Renomeie o arquivo `.env.example` para `.env`.

2.  **Adicione sua chave de API:**
    Abra o arquivo `.env` e insira sua chave de API da Groq.
    ```
    GROQ_API_KEY="sua_chave_de_api_aqui"
    ```
    Você pode obter uma chave gratuita no [site da Groq](https://console.groq.com/keys).

## Uso

1.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```
    A aplicação estará disponível em `http://127.0.0.1:8000`.

2.  **Acesse a interface:**
    Abra o seu navegador e acesse `http://127.0.0.1:8000`.

3.  **Envie os arquivos XML:**
    - Clique em "Escolher arquivos" e selecione as NF-es que deseja processar.
    - Clique no botão "Gerar relatório".
    - O sistema processará os arquivos e fornecerá um link para baixar o relatório em Excel.

4.  **Gere o Resumo com IA (Opcional):**
    - Após gerar o relatório, um botão "Gerar resumo IA" aparecerá.
    - Clique nele para que a inteligência artificial analise o conteúdo do relatório e exiba um resumo na tela.

## Endpoints da API

A documentação completa da API (Swagger UI) está disponível em `http://127.0.0.1:8000/docs`.

- `POST /processar-nfes`: Envia uma lista de arquivos XML e retorna os totais e o nome do arquivo de relatório Excel gerado.
- `GET /download-relatorio`: Faz o download do relatório Excel. Requer o parâmetro `nome_arquivo`.
- `GET /resumo-ia`: Gera e retorna o resumo em texto dos dados de um relatório Excel. Requer o parâmetro `nome_arquivo`.
- `GET /health`: Endpoint para verificar se a aplicação está no ar.
