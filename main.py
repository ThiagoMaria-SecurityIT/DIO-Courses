import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
from dotenv import load_dotenv

load_dotenv()

# Configurações do Azure
BlobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobaccountName = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER = os.getenv('SQL_SERVER')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# Título da aplicação
st.title('Cadastro de Produtos')

# Inicializar session_state para limpeza de formulário
if 'product_name' not in st.session_state:
    st.session_state.product_name = ""
if 'product_price' not in st.session_state:
    st.session_state.product_price = 0.0
if 'product_description' not in st.session_state:
    st.session_state.product_description = ""
if 'product_image' not in st.session_state:
    st.session_state.product_image = None

# Função para upload no blob storage
def upload_blob(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
        container_client = blob_service_client.get_container_client(blobContainerName)
        blob_name = str(uuid.uuid4()) + file.name
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        image_url = f"https://{blobaccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro no upload do blob: {e}")
        return ""

# Função para inserir produto no SQL Server
def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES (%s, %s, %s, %s)",
            (product_name, product_price, product_description, image_url)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao inserir produto: {e}')
        return False

# Função para listar produtos do SQL Server
def list_products():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor(as_dict=True)
        query = "SELECT id, nome, descricao, preco, imagem_url FROM dbo.Produtos"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

# Função para deletar imagem do Azure Blob
def delete_blob(blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
        container_client = blob_service_client.get_container_client(blobContainerName)
        blob_client = container_client.get_blob_client(blob_name)

        if blob_client.exists():
            blob_client.delete_blob()
            st.success(f"🖼️ Imagem '{blob_name}' excluída do Blob Storage.")
        else:
            st.warning(f"⚠️ Imagem '{blob_name}' não encontrada.")
    except Exception as e:
        st.error(f"❌ Erro ao excluir imagem: {e}")

# Função para deletar produto do SQL Server
def delete_product_from_sql(product_id):
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Produtos WHERE id = %d", (product_id,))
        conn.commit()
        conn.close()
        st.success("🗑️ Produto excluído do banco de dados.")
    except Exception as e:
        st.error(f"❌ Erro ao excluir produto do banco: {e}")

# Abas para navegação
tabs = st.tabs(["Cadastro", "Listagem"])

# Aba de Cadastro
with tabs[0]:
    st.header("Cadastro de Produtos")

    # Formulário dentro do placeholder
    product_name = st.text_input('Nome do Produto', value=st.session_state.product_name)
    product_price = st.number_input('Preço do Produto', min_value=0.0, format='%.2f', value=st.session_state.product_price)
    product_description = st.text_area('Descrição do Produto', value=st.session_state.product_description)
    product_image = st.file_uploader('Imagem do Produto', type=['jpeg', 'png', 'jpg'], key="file_uploader")

    if st.button('Salvar Produto'):
        if not product_name or product_price is None or not product_description or not product_image:
            st.warning("Preencha todos os campos e selecione uma imagem.")
        else:
            sucesso = insert_product(product_name, product_price, product_description, product_image)
            if sucesso:
                st.success("✅ Produto salvo com sucesso!")
            
            # Resetar os campos usando session_state
            st.session_state.product_name = ""
            st.session_state.product_price = 0.0
            st.session_state.product_description = ""
            st.session_state.product_image = None
            st.rerun()

# Aba de Listagem
with tabs[1]:
    st.header("Listagem de Produtos")

    if st.button('Listar Produtos'):
        st.session_state.products_list = list_products()
        st.rerun()

    products = st.session_state.get("products_list", list_products())

    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["imagem_url"]:
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200">'
                    st.markdown(html_img, unsafe_allow_html=True)

                # Botão Excluir
                if st.button("🗑️ Excluir", key=f"delete_{product['id']}"):
                    blob_name = product["imagem_url"].split("/")[-1]
                    delete_blob(blob_name)
                    delete_product_from_sql(product['id'])
                    st.rerun()

                st.markdown("---")
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado.")