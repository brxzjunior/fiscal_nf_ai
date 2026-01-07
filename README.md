# FiscalIA Pro

FiscalIA Pro é uma aplicação web para análise inteligente de Notas Fiscais Eletrônicas (NF-e) em formato XML. A ferramenta extrai dados de múltiplos arquivos, gera um relatório consolidado em Excel e oferece um resumo analítico criado por Inteligência Artificial.

![Logo da Aplicação](assets/logoai.png)

## Funcionalidades

- **Upload de Múltiplos Arquivos:** Envie um ou mais arquivos XML de NF-e de uma só vez.
- **Extração de Dados:** O sistema extrai automaticamente informações essenciais como CNPJ do emitente, nome do emitente, valor total da nota e valor do ICMS.
- **Relatório em Excel:** Gera um arquivo `.xlsx` com os dados organizados, incluindo uma linha de totais.
- **Análise com IA:** Utiliza a API da Groq com o modelo Llama 3.3 70B para gerar um resumo inteligente dos dados, destacando os principais emissores e a concentração de ICMS.
- **Interface Moderna:** Frontend responsivo e intuitivo para uma ótima experiência de usuário.

## Como Usar

### 1. Pré-requisitos

- Python 3.8+
- [Git](https://git-scm.com/)

### 2. Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd fiscal_ai_pro
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv fiscalia_env
    source fiscalia_env/bin/activate  # No Windows: fiscalia_env\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    - Crie um arquivo chamado `.env` na raiz do projeto (pode copiar o `.env.example`).
    - Adicione sua chave da API da Groq ao arquivo `.env`:
      ```
      GROQ_API_KEY="sua_chave_aqui"
      ```

### 3. Execução

1.  **Inicie o servidor:**
    ```bash
    uvicorn main:app --reload
    ```

2.  **Acesse a aplicação:**
    - Abra seu navegador e acesse [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 4. Utilizando a Interface

1.  **Carregue os arquivos:** Arraste e solte os arquivos XML na área de upload ou clique para selecioná-los.
2.  **Gere o relatório:** Clique no botão "Gerar Relatório".
3.  **Visualize os resultados:** A aplicação exibirá a quantidade de notas processadas e os totais.
4.  **Baixe o Excel:** Clique em "Baixar Excel" para obter o relatório detalhado.
5.  **Análise com IA:** Clique em "Gerar Resumo IA" para ver a análise gerada pela inteligência artificial.

## Tecnologias Utilizadas

- **Backend:**
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Pandas](https://pandas.pydata.org/)
  - [Openpyxl](https://openpyxl.readthedocs.io/en/stable/)
  - [Uvicorn](https://www.uvicorn.org/)
- **Inteligência Artificial:**
  - [Groq API](https://groq.com/) (modelo Llama 3.3 70B)
- **Frontend:**
  - HTML5, CSS3, JavaScript (vanilla)

## Estrutura do Projeto

```
.
├── .env.example
├── .gitignore
├── ia_agente.py      # Módulo da IA para gerar resumos
├── main.py           # Arquivo principal com a lógica do FastAPI e o frontend
├── requirements.txt  # Dependências do Python
├── assets/           # Ícones e logos
└── ...
```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.