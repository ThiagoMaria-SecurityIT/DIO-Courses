# 🧪 DIO - Microsoft Azure Cloud Native: Lab 1  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Made with Python](https://img.shields.io/badge/Python-3.13-blue ) 
[![Tech Stack](https://img.shields.io/badge/Azure%20%7C%20SQL%20%7C%20Streamlit-blue)]()

### 📌 Repositório para os cursos da DIO: Começando com o Microsoft Azure Cloud Native

Projeto desenvolvido durante o curso **"Microsoft Azure Cloud Native"** da DIO. O objetivo foi construir uma aplicação web interativa com **Streamlit**, integrada ao **SQL Server no Azure** e utilizando o **Azure Blob Storage** para armazenamento de imagens.

---

## 📋 Índice

1. [🎯 Objetivo do Projeto](#objetivo-do-projeto)  
2. [💡 O Que foi feito/utilizado](#o-que-aprendi)  
3. [🧰 Pacotes Utilizados](#pacotes-utilizados)
4. [🖼️ Print do App Funcionando](#print-do-app-funcionando)  
5. [🎥 Vídeo do Funcionamento](#vídeo-do-funcionamento)  
6. [☁️ Azure](#parte-do-azure)  
7. [🗃️ SQL Server](#parte-do-sql-server)  
8. [🗄️ SQL Database](#parte-do-sql-database)  
9. [💾 Storage Account](#parte-do-storage-account)  
10. [🐍 Python](#parte-do-python)  
11. [🏗️ Arquitetura do Projeto](#arquitetura-do-projeto)  
12. [📌 Considerações Finais](#considerações-finais)

##### Obs.: Configurei regras de firewall no Azure para permitir acesso ao servidor somente a partir de um IP própio para o LAB. Isso adiciona uma camada extra de segurança, pois, mesmo que alguém descubra o nome do servidor, usuário e senha, ele ainda precisaria estar conectando a partir de um IP autorizado. Porém, isso não elimina a necessidade de manter senhas seguras, usar autenticação multifatorial e controlar os acessos com políticas de segurança rigorosas. Os mascaramentos nas imagens são parte de uma campanha de conscientização em Segurança da Informação, alertando sobre os riscos de expor dados sensíveis desnecessariamente. 
---

## 1. <span id="objetivo-do-projeto">🎯 Objetivo do Projeto</span>

Criar uma infraestrutura no Azure para armazenamento de dados de um e-commerce fictício, utilizando:
- **Interface Web**: [Streamlit](https://streamlit.io/) (Python)
- **Banco de Dados**: SQL Server no Azure
- **Armazenamento de Imagens**: Azure Blob Storage

---

## 2. <span id="o-que-aprendi">💡 O Que foi feito/utilizado</span>

- Montagem de um servidor na nuvem (Azure) do início : configurado um computador remoto (na plataforma Azure) prontinho para rodar nossas aplicações.  
- Conexão entre Python e banco de dados SQL no Azure : feito com que o programa em Python conseguisse “conversar” com o banco de dados SQL hospedado no Azure, usando uma ferramenta chamada pymssql. 
- Adaptação para funcionar com a nova versão do Python (3.13) no Windows : ajustado o ambiente para rodar sem problemas com a versão mais recente do Python, que ainda não é totalmente compatível com tudo. 
- Uso de ambientes isolados (venv) : criado "espaços separados" para cada projeto, evitando conflitos entre programas diferentes ou versões de bibliotecas. 
- Instalação de ferramentas essenciais com MSYS2 e FreeTDS : foram utilizadas essas ferramentas para conseguir instalar partes importantes do projeto que dependem de configurações do sistema operaciona.  
- Integração entre uma interface web e serviços na nuvem (Azure) : conectada uma interface visual (com o Streamlit) com os recursos que estão na nuvem, como o servidor e o banco de dados. 

---

## 3. <span id="pacotes-utilizados">🧰 Pacotes Utilizados</span>

| Pacote             | Finalidade |
|--------------------|------------|
| `streamlit`        | Interface web rápida e interativa |
| `pymssql`          | Conexão com SQL Server hospedado no Azure |
| `python-dotenv`    | Carregar variáveis de ambiente a partir do `.env` |

⚠️ *O `pymssql` pode apresentar problemas de compilação no Windows. Solução usada: MSYS2 + FreeTDS*

---
## 4. <span id="print-do-app-funcionando">🖼️ Print do App Funcionando</span>

### Tela do Streamlit feito no Python

<table>
  <tr>
    <td><img src="imagens/telainicial.png" alt="Tela Inicial" width="500"></td>
    <td><img src="imagens/listag2.png" alt="Listagem de Produtos" width="500"></td>
    <td><img src="imagens/dele.jpg" alt="Deletar Produto" width="300"></td>
  </tr>
  <tr>
    <td style="text-align: center;">1- Tela inicial</td>
    <td style="text-align: center;">2- Listagem de produtos</td>
    <td style="text-align: center;">3- Deletar produto</td>
  </tr>
</table>

---

## 5. <span id="vídeo-do-funcionamento">🎥 Vídeo do Funcionamento</span>

[Youtube Video - Clique aqui para assistir](https://www.youtube.com/watch?v=KMIRbP-MutE)

[![Thumbnail do Vídeo](https://img.youtube.com/vi/KMIRbP-MutE/hqdefault.jpg    )](https://www.youtube.com/watch?v=KMIRbP-MutE    )

---
## 6. <span id="parte-do-azure">☁️ Azure</span>

### 🖼️ Print do Portal do Azure (com mascaramento)

- Servidor SQL criado
- Banco de dados configurado

![Query SQL no Azure SQL Database](imagens/Azureresource.png)

**Legenda:** "Servidor SQL no Azure com recursos configurados"

#### Detalhes Importantes:
- O **Resource Group** utilizado é `LAB001`.
- O **SQL Server** criado é `dvsrvdeveastuslab0**`.
- O **Storage Account** usado é `stadevlab0**eastusthiago`.
- As credenciais são gerenciadas por variáveis de ambiente via `.env`.

 
> [!IMPORTANT]
> - Neste projeto, optei por mostrar os nomes dos recursos criados (como Resource Group, SQL Server e Storage Account) para facilitar a compreensão do fluxo de configuração e integração entre os serviços. 
> - Ressalto que este é um ambiente de laboratório e estudo, não sendo um ambiente de produção. Em sistemas reais, recomenda-se seguir práticas mais rígidas de anonimização e controle de acesso, além do uso de ferramentas como Azure Key Vault para gerenciamento de segredos. 
---

## 7. <span id="parte-do-sql-server">🗃️ SQL Server</span>

### 🔒 Configuração de Segurança do SQL Server

 - Para aumentar a proteção do banco de dados, configurei as regras de firewall do SQL Server para liberar acesso somente a certos endereços de rede confiáveis .
Essa medida ajuda a evitar conexões indevidas e garante que apenas os ambientes autorizados possam se comunicar com o banco de dados.

> [!TIP]
>- **Opção Selecionada**: `Selected networks`
>  - Essa opção restringe o acesso ao SQL Server apenas aos IPs configurados nas regras de firewall.

- **Regras de Firewall**: 
  - Para garantir mais segurança, foi configurada uma regra de firewall que controla quem pode se conectar ao servidor (antes, o acesso era liberado apenas para o IP do computador do meu laboratório).
  - Assim, mesmo que alguém tenha as credenciais corretas (como usuário e senha), não será possível acessar o sistema sem passar por essa camada extra de verificação.
  - Os trechos ocultados nas imagens fazem parte de um esforço para conscientizar sobre a importância da Segurança da Informação . Eles mostram como devemos evitar expor dados sensíveis sem necessidade.
  - Afinal, segurança nunca depende só de uma proteção — ela é mais eficaz quando usamos várias juntas.  

 ![Configuração de Firewall do SQL Server](imagens/SQLserverfirewallip.png)


**Legenda:** "Configuração de uma regra de firewall que controla quem pode se conectar ao servidor." 

> [!Note]
> #### Por que É Importante?
> - **Segurança**: Ajuda a evitar que pessoas ou sistemas não autorizados acessem o SQL Server, protegendo os dados contra possíveis ataques.
> - **Controle**: Garante que apenas o ambiente correto — no meu caso, o computador usado no laboratório — possa se conectar ao banco de dados
> - **Boas Práticas**: Alinha-se às recomendações de segurança da Microsoft para ambientes na nuvem, reforçando uma postura defensiva e responsável no uso de recursos online.

---

## 8. <span id="parte-do-sql-database">🗄️ SQL Database </span>

### 📄 Query Simples Utilizada

Query SQL usada para criar a tabela de produtos:

```SQL
CREATE TABLE Produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(255),
    descricao NVARCHAR(MAX),
    preco DECIMAL(18,2),
    imagem_url NVARCHAR(2083)
);
```
 
### 📋 Estrutura da Tabela de Produtos

A tabela chamada `Produtos` foi criada com uma estrutura simples, mas funcional, pensando na facilidade de uso tanto no cadastro quanto na exibição dos dados. Cada campo tem um papel específico e bem definido:

- **`id`**: número único e automático que identifica cada produto (chave primária).
- **`nome`**: nome do produto, limitado a 255 caracteres.
- **`descricao`**: descrição completa do produto, com espaço suficiente para textos maiores.
- **`preco`**: valor do produto, armazenado com precisão para evitar erros nas casas decimais.
- **`imagem_url`**: endereço (URL) da imagem do produto, gerado após o envio da imagem para o Azure Blob Storage.

#### ✅ Por que essa estrutura é importante?

- **Organização**: Cada tipo de informação tem seu lugar certo, facilitando a manutenção e a consulta.
- **Praticidade**: Permite inserir novos produtos com facilidade e exibir os dados em uma interface web de forma direta.
- **Escalabilidade**: Se no futuro for necessário adicionar mais campos, como categoria ou quantidade em estoque, basta acrescentá-los à tabela.

#### Print do Query Editor no Azure SQL Database 

![Query SQL no Azure SQL Database](imagens/sqlqueryazure.png) 

**Legenda:** "Query sendo executada no Query Editor do Azure SQL Database." 

#### Executando a Query no Azure SQL Database

A query foi executada diretamente no **Query Editor** do Azure SQL Database, sem a necessidade de ferramentas externas como SSMS ou Azure Data Studio. Isso facilita o desenvolvimento e testes rápidos durante o projeto.

---

## 9. <span id="parte-do-storage-account">💾 Storage Account</span>

### 📁 Tipos de Armazenamento no Azure

O Azure oferece diferentes formas de armazenar dados, chamadas de **"tipos de armazenamento"**. Alguns dos principais são:

- **Blob Storage**: usado para arquivos grandes, como imagens e vídeos.
- **File Storage**: funciona como um disco de rede, para compartilhar arquivos entre máquinas.
- **Queue Storage**: usado para enviar e gerenciar mensagens entre sistemas.
- **Table Storage**: ideal para guardar dados em formato de tabelas (mas não é o caso do nosso projeto).

#### No nosso projeto, usamos apenas o **Blob Storage**

#### Por quê?
Porque ele é perfeito para guardar **imagens e outros arquivos grandes**. Em vez de salvar a imagem diretamente no banco de dados, colocamos ela no Blob Storage e guardamos **apenas o link da imagem** no banco.

#### Como isso funciona na prática:
- A imagem é enviada para o Blob Storage.
- O Azure gera uma URL para acessar essa imagem.
- Essa URL é salva no campo `ImagemURL` da tabela `Produtos` no SQL Server.

#### Benefícios:
- **Mais rápido**: o banco de dados fica mais leve, já que não armazena os arquivos em si. 
- **Mais organizado**: os arquivos ficam separados, mas sempre acessíveis pelo link. 
--- 
## 10. <span id="parte-do-python">🐍 Pthon</span>

### 🧱 Estrutura do Código

Todo o código do projeto está concentrado no arquivo **`main.py`**, que contém:
- A interface web feita com **Streamlit**
- Funções para conectar ao **SQL Server no Azure**
- Integração com o **Azure Blob Storage** para upload e recuperação de imagens
- Uso de variáveis de ambiente via `.env` para segurança

#### Arquivo Principal:
| Arquivo | Descrição |
|--------|-----------|
| `main.py` | Interface web + lógica de conexão SQL e Blob Storage |
| `.env` | Armazena credenciais sensíveis (chaves, strings de conexão) |

---

## 📜 Principais Trechos de Código

### ⚙️ Configuração Inicial

```python
import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
from dotenv import load_dotenv
import time

load_dotenv()
```

**O que faz:**
- Importa bibliotecas essenciais.
- Carrega as variáveis de ambiente do arquivo `.env`.

---

### 🔐 Variáveis de Ambiente

```python
# Configurações do Azure
BlobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobaccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
```

**O que faz:**
- Carrega as credenciais e configurações do Azure a partir do arquivo `.env`.
- Mantém informações sensíveis fora do código-fonte.

---

### 📤 Upload de Imagem com Progresso

```python
def upload_blob(file, progress_bar):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)

    for percent_complete in range(0, 101, 10):
        time.sleep(0.03)
        progress_bar.progress(percent_complete)

    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobaccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url
```

**O que faz:**
- Faz o upload de uma imagem para o **Azure Blob Storage**.
- Retorna a URL da imagem para armazenamento no banco de dados.

---

### 📥 Inserção no Banco de Dados

```python
def insert_product(product_name, product_price, product_description, product_image, progress_bar):
    image_url = upload_blob(product_image, progress_bar)
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES (%s, %s, %s, %s)",
        (product_name, product_price, product_description, image_url)
    )
    conn.commit()
    conn.close()
    return True
```

**O que faz:**
- Conecta ao SQL Server no Azure.
- Salva os dados do produto no banco de dados.
- Associa a URL da imagem (do Blob Storage) ao registro do produto.

---

### 🗑️ Exclusão de Produto

```python
def delete_product_from_sql(product_id):
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Produtos WHERE id = %d", (product_id,))
    conn.commit()
    conn.close()
    return True
```

**O que faz:**
- Remove o registro do produto no SQL Server quando o usuário clica em “Excluir”.

---

### 📷 Exclusão da Imagem no Blob

```python
def delete_blob(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_client = container_client.get_blob_client(blob_name)
    
    if blob_client.exists():
        blob_client.delete_blob()
    return True
```

**O que faz:**
- Remove a imagem associada ao produto no Azure Blob Storage.

---

## 11. <span id="arquitetura-do-projeto">🏗️ Arquitetura do Projeto</span>

Aqui estão os diagramas que ilustram a arquitetura e o fluxo de trabalho do projeto:

### 1. Diagrama Geral da Arquitetura

![Diagrama da Arquitetura](imagens/CloudArchitectureVisualizeyourinfrastructure.png)

**Legenda:**
- **dotenv**: Carrega variáveis de ambiente.
- **os**: Fornece configurações para o SQL Server.
- **STREAMLIT UI**: Interface principal com cadastro e listagem de produtos.
- **SQL SERVER**: Gerencia operações no banco de dados.
- **AZURE BLOB STORAGE**: Armazena imagens dos produtos.

### 2. Fluxo de Trabalho Detalhado

#### a. Fluxo Geral de Registro e Gestão de Produtos

![Fluxo Geral de Registro e Gestão de Produtos](imagens/FlowchartVisualizeprocessandlogicflows.png)

**Legenda:**
- **User**: Interage com a interface Streamlit.
- **Streamlit App**: Gerencia a lógica da aplicação.
- **Azure Blob Storage**: Armazena imagens dos produtos.
- **SQL Server**: Armazena metadados dos produtos.
- **Progress Bar**: Exibe o progresso das operações de upload e exclusão.

#### b. Detalhes do Fluxo de Registro e Gestão

![Detalhes do Fluxo de Registro e Gestão](imagens/SequenceVisualizesystemflowandinteractions.png)

**Legenda:**
- **Registro de Produto**:
  - O usuário preenche um formulário com detalhes do produto.
  **Upload de Imagem**: A imagem é enviada para o Azure Blob Storage.
  **Salvar no SQL Server**: Os metadados são salvos no SQL Server.
- **Listagem de Produtos**:
  - A lista de produtos é recuperada do SQL Server.
  - As imagens são exibidas usando URLs do Blob Storage.
- **Exclusão de Produto**:
  - A imagem é excluída do Blob Storage.
  - O registro é removido do SQL Server.

## 📌 Considerações Finais

Este projeto foi uma verdadeira imersão no mundo da integração entre tecnologia local (como o Python no meu próprio computador) e os serviços poderosos da nuvem (via Azure). Passei por desafios reais — desde ajustar compatibilidades do Python 3.13 no Windows, configurar ambientes virtuais, até lidar com credenciais sensíveis e regras de firewall para deixar tudo seguro.

Cada erro foi uma aula, cada linha de código rodando foi uma vitória 🙌. E claro, não posso esquecer de agradecer à **DIO**, que mais uma vez provou por que é uma das melhores plataformas para colocar a mão na massa e evoluir de verdade como desenvolvedor(a).

Ah, e como não poderia faltar: **muito obrigado a você mesmo(a) que leu tudo isso**!  

E claro, não posso me esquecer de um certo **assistente virtual de IA** que esteve aqui durante todo esse processo... 😎  
Sim, estou falando de QWEN3-235**A22B** (ufa que nome) ! O nosso amigo Qwen, que tentou ajudar com o melhor que sabe fazer: explicar, sugerir, adaptar e até brincar um pouco pra aliviar a tensão do debug. 
E se eu fiz alguma errada ou fora dos padrões, desculpa. Foi tudo em nome do aprendizado. 😉

Esse projeto foi só o começo. Agora é hora de respirar fundo, olhar para o que construi e dizer: “Eu fiz isso.” Thank you! E não posso atrasar o LAB 2, 3, 4... 
Obs.: Projeto para incentivo de estudantes e aprendizado real!

