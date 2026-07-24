import streamlit as st
import pandas as pd

# Configuração da página (largura total e título da aba)
st.set_page_config(page_title="Gestão de Vistorias", layout="centered")

st.title("📋 Formulário de Vistoria de Imóveis")

# --- CONEXÃO COM O SHAREPOINT (Estrutura Base) ---
# Dica: As credenciais do SharePoint ficarão nas variáveis secretas do Streamlit Cloud
# por segurança, e não no código visível do GitHub.

@st.cache_data(ttl=600)  # Mantém os dados no cache por 10 min para rodar ultra rápido
def carregar_imoveis():
    # Exemplo simulado - Aqui trocaremos pela leitura da sua Lista do SharePoint
    dados = [
        {"Title": "Rua Conselheiro Nébias 1270, Apto 72", "SQL": "123.456.789", "Bairro": "Campos Elíseos", "CEP": "01203-002"},
        {"Title": "Rua Barão de Tatuí 109, Apto 71", "SQL": "987.654.321", "Bairro": "Vila Buarque", "CEP": "01226-000"}
    ]
    return pd.DataFrame(dados)

df_imoveis = carregar_imoveis()

# --- INTERFACE DO FORMULÁRIO ---

# 1. Campo com Busca Dinâmica (digite o endereço e ele filtra)
lista_enderecos = df_imoveis["Title"].tolist()
endereco_selecionado = st.selectbox(
    "Digite ou selecione o Endereço do Imóvel:", 
    options=lista_enderecos, 
    index=None,
    placeholder="Comece a digitar o nome da rua ou número..."
)

# 2. Atualização Automática dos Dados do Imóvel Selecionado
if endereco_selecionado:
    # Filtra a linha exata do imóvel no DataFrame
    imovel = df_imoveis[df_imoveis["Title"] == endereco_selecionado].iloc[0]
    
    st.markdown("---")
    st.subheader("Dados do Imóvel")
    
    # Exibe os campos preenchidos automaticamente
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("SQL", value=imovel["SQL"], disabled=True)
        st.text_input("Bairro", value=imovel["Bairro"], disabled=True)
    with col2:
        st.text_input("CEP", value=imovel["CEP"], disabled=True)
    
    st.markdown("---")
    st.subheader("Detalhes da Vistoria")
    
    # Campos para preenchimento da vistoria
    status = st.selectbox("Status da Vistoria", ["Em Andamento", "Aprovado com Restrições", "Aprovado"])
    observacoes = st.text_area("Observações Gerais")
    fotos = st.file_uploader("Anexar Fotos do Imóvel", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    # Botão de Envio
    if st.button("💾 Salvar Relatório de Vistoria", type="primary"):
        st.success(f"Vistoria do imóvel '{endereco_selecionado}' salva com sucesso!")
