# ETL Sales Pipeline - Integração REST API & Google Sheets 🚀

O **ETL Sales Pipeline** é um pipeline automatizado de Extração, Transformação e Carga (ETL) desenvolvido em **Python**. Ele foi projetado para consumir dados de vendas e carrinhos a partir de APIs RESTful externas, realizar o tratamento e estruturação dos dados em lote e persisti-los diretamente no **Google Sheets**, atuando como um banco de dados leve ou repositório de relatórios gerenciais em tempo real.

A solução utiliza autenticação segura via **Service Account (OAuth2 / Google Cloud IAM)**, manipulação de dados em memória com **Pandas**, gerenciamento dinâmico de variáveis de ambiente com **python-dotenv** e integração direta com a **Google Sheets API v4** via **gspread**.

---

## 🏗️ Arquitetura do Ecossistema ETL

A solução é composta por módulos bem definidos seguindo o padrão **Controller/Service Layer** para separação de responsabilidades:

```
ETL---Python/
├── meu_projeto_etl/
│   ├── src/
│   │   ├── controller/
│   │   │   └── sheets.py       # SheetsController: Gerencia autenticação OAuth2 e escrita no Google Sheets
│   │   └── services/           # Regras de negócio e serviços auxiliares
│   ├── etls.py                 # Módulo experimental / manipulação de CSVs com Pandas
│   ├── main.py                 # Orquestrador do fluxo ETL (Extração, Transformação e Carga)
│   ├── requirements.txt        # Dependências do ecossistema Python
│   └── vendas.csv              # Massa de dados local para testes/ingestão
├── .gitignore                  # Regras de proteção de credenciais e arquivos sensíveis
└── README.md                   # Documentação oficial do repositório
```

### 📦 Componentes Principais

* **Extractor (API / DummyJSON)**: Consome endpoints HTTP REST (`https://dummyjson.com/carts`) utilizando a biblioteca `requests`, tratando exceções de rede com `raise_for_status()` e normalizando payloads JSON complexos contendo estruturas aninhadas de carrinhos e produtos.
* **Transformer (Flattening & Normalização)**: Desestrutura objetos relacionais 1:N (1 Carrinho para N Produtos) criando uma matriz tabular limpa com os campos: `[ID Carrinho, ID Usuário, Produto, Preço, Quantidade, Total]`.
* **SheetsController (Google Sheets Integration)**:
  * **Autenticação Segura**: Utiliza Service Account do Google Cloud Platform com escopo limitado de `spreadsheets`.
  * **Carregamento Dinâmico**: Localiza o arquivo de chave privada `credentials.json` via resolução de caminhos com `pathlib`.
  * **Operações em Lote (Batching)**: Métodos para escrita de cabeçalho (`insert_row`), inserção individual (`append_row`) e carga massiva de registros (`append_rows`).

---

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de possuir:

* **Python 3.8+** instalado na sua máquina.
* Uma **Conta Google Cloud** com a API **Google Sheets API** ativada.
* Uma planilha criada no **Google Sheets** onde os dados serão gravados.

---

## 🚀 Como Executar o Projeto

### 1. Configurar as Variáveis de Ambiente e Credenciais

O projeto utiliza variáveis de ambiente e arquivos de credenciais para garantir a segurança da informação.

#### A. Arquivo `.env`
Crie um arquivo `.env` no diretório `meu_projeto_etl/` contendo a chave da planilha destino:

```env
GOOGLE_SHEET_ID=sua_id_da_planilha_aqui
```

> **Como obter o `GOOGLE_SHEET_ID`**: Abra sua planilha no navegador. A URL terá o formato:  
> `https://docs.google.com/spreadsheets/d/`**`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`**`/edit#gid=0`  
> Copie a sequência de caracteres entre `/d/` e `/edit`.

---

### 🔑 Guia Completo para Configurar a Service Account (Google Cloud)

#### 1. Criar Projeto e Ativar a API do Google Sheets
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto (ex: `ETL-Sales-Pipeline`).
3. No menu lateral, navegue até **APIs e Serviços > Biblioteca**.
4. Pesquise por **Google Sheets API** e clique em **Ativar**.

#### 2. Criar a Conta de Serviço (Service Account)
1. Vá para **APIs e Serviços > Credenciais**.
2. Clique em **+ Criar Credenciais** e selecione **Conta de Serviço**.
3. Defina um nome para a conta (ex: `sheets-writer`) e clique em **Criar e Continuar**.
4. Na tela seguinte, conceda o papel de **Editor** ou avance até finalizar.

#### 3. Baixar a Chave JSON (`credentials.json`)
1. Na lista de Contas de Serviço criadas, clique na conta recém-criada.
2. Navegue até a aba **Chaves** (Keys) > **Adicionar Chave** > **Criar nova chave**.
3. Selecione o formato **JSON** e clique em **Criar**.
4. Um arquivo `.json` será baixado no seu computador.
5. Renomeie esse arquivo para `credentials.json` e mova-o para a raiz do seu projeto (`meu_projeto_etl/credentials.json`).

⚠️ **Importante**: Nunca envie o arquivo `credentials.json` ou o `.env` para o GitHub! O repositório já conta com o `.gitignore` pré-configurado para ignorá-los.

#### 4. Compartilhar a Planilha com a Service Account
1. Abra o arquivo `credentials.json` e copie o e-mail contido no campo `"client_email"` (ex: `sheets-writer@seu-projeto.iam.gserviceaccount.com`).
2. Abra a sua planilha no **Google Sheets**.
3. Clique no botão **Compartilhar** (canto superior direito) e adicione o e-mail da Service Account com permissão de **Editor**.

---

### 2. Instalar as Dependências

Crie um ambiente virtual (opcional, porém recomendado) e instale as bibliotecas necessárias:

```bash
# Criar e ativar o ambiente virtual (Windows)
python -m venv venv
.env\Scriptsctivate

# Instalar dependências do projeto
pip install -r meu_projeto_etl/requirements.txt
```

---

### 3. Executar o Pipeline ETL

Com o ambiente configurado, rode o orquestrador principal:

```bash
python meu_projeto_etl/main.py
```

**Saída esperada no terminal:**
```text
iniciando teste de conexão...
Conectado com sucesso à planilha: Página1
Total de registros extraídos: 30
{'id': 1, 'products': [...]}
```

---

## 🧪 Estrutura de Ingestão de Dados

### Schema do Cabeçalho Gerado

Ao executar o pipeline, os dados são desestruturados e organizados nas seguintes colunas na planilha:

| ID Carrinho | ID Usuário | Produto | Preço | Quantidade | Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `1` | `168` | `Essence Mascara Lash Princess` | `9.99` | `2` | `19.98` |
| `1` | `168` | `Eyeshadow Palette with Mirror` | `19.99` | `1` | `19.99` |

---

## 📝 Detalhes e Diferenciais Técnicos

1. **Abstração de Controladores (`SheetsController`)**:
   A comunicação com a API do Google Sheets foi isolada em uma classe gerenciadora (`SheetsController`), facilitando reuso de código, testes e manutenção modular.
2. **Resolução Dinâmica de Diretórios (`pathlib.Path`)**:
   Utiliza a biblioteca padrão `pathlib` para localizar o arquivo de credenciais independentemente do sistema operacional (Windows/Linux) ou do diretório onde o script foi invocado.
3. **Escopo Mínimo Privilegiado (Security Best Practices)**:
   A autenticação solicita permissões restritas aos escopos necessários da API (`spreadsheets`), aderindo ao princípio de menor privilégio (PoLP).
4. **Transformação Estruturada em Memória**:
   Processa payloads JSON aninhados em uma lista de tuplas achatadas (`flat matrix`), reduzindo a quantidade de chamadas I/O à API e otimizando a taxa de cota da quota do Google API.

---

Desenvolvido por **Alexandre Coelho dos Santos Brito**  
🔗 GitHub: [91061730](https://github.com/91061730)
