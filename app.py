import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Gestão de Imóveis & Vistorias", layout="wide", page_icon="🏢")

st.title("🏢 Sistema de Gestão Imobiliária")

# Menu de Navegação na Barra Lateral
menu = st.sidebar.radio(
    "Navegação / Formulários:",
    ["1. Gestão de Imóveis (Criar/Editar)", "2. Realizar Vistoria", "3. Registro de Manutenção"]
)

# --- DADOS DE EXEMPLO (Simulação enquanto não conecta ao SharePoint) ---
if "imoveis_mock" not in st.session_state:
    st.session_state["imoveis_mock"] = [
        {"Title": "Rua Conselheiro Nébias 1270, Apto 72", "Bairro": "Campos Elíseos", "Regiao": "Centro", "SQL": "123.456.789", "Tipo": "Apartamento"},
        {"Title": "Rua Barão de Tatuí 109, Apto 71", "Bairro": "Vila Buarque", "Regiao": "Centro", "SQL": "987.654.321", "Tipo": "Apartamento"}
    ]

lista_enderecos = [i["Title"] for i in st.session_state["imoveis_mock"]]
lista_bairros_existentes = list(set([i["Bairro"] for i in st.session_state["imoveis_mock"]]))

# ==============================================================================
# FORMULÁRIO 1: GESTÃO DE IMÓVEIS (Criação e Edição)
# ==============================================================================
if menu == "1. Gestão de Imóveis (Criar/Editar)":
    st.header("📝 Cadastrar ou Editar Imóvel")
    
    modo = st.radio("Ação:", ["Novo Imóvel", "Editar Existente"], horizontal=True)
    
    imovel_sel = None
    if modo == "Editar Existente":
        end_busca = st.selectbox("Selecione o Imóvel para Editar:", lista_enderecos, index=None)
        if end_busca:
            imovel_sel = next(item for item in st.session_state["imoveis_mock"] if item["Title"] == end_busca)

    with st.form("form_imovel", clear_on_submit=False):
        st.subheader("Informações Principais")
        
        col1, col2 = st.columns(2)
        with col1:
            endereco = st.text_input("Endereço (Título):", value=imovel_sel["Title"] if imovel_sel else "")
            
            # Bairro: Selecionar ou digitar novo
            bairro_opcao = st.selectbox("Selecione um Bairro existente:", ["-- Digitar outro --"] + lista_bairros_existentes)
            if bairro_opcao == "-- Digitar outro --":
                bairro = st.text_input("Digite o novo Bairro:", value=imovel_sel["Bairro"] if imovel_sel else "")
            else:
                bairro = bairro_opcao
                
            cep = st.text_input("CEP:", value=imovel_sel.get("CEP", "") if imovel_sel else "")
            regiao = st.selectbox("Região:", ["Norte", "Sul", "Leste", "Oeste", "Centro"])
            
        with col2:
            tipo = st.selectbox("Tipo do Imóvel:", ["Apartamento", "Casa", "Prédio", "Sala Comercial", "Terreno", "Vaga de Garagem", "Loja"])
            sql = st.text_input("SQL:", value=imovel_sel["SQL"] if imovel_sel else "")
            area_util = st.number_input("Área Útil (m²):", min_value=0.0, step=1.0)
            area_total = st.number_input("Área Total (m²):", min_value=0.0, step=1.0)

        st.markdown("---")
        st.subheader("Mídias e Detalhes")
        
        fachada = st.file_uploader("Foto da Fachada:", type=['png', 'jpg', 'jpeg'])
        fotos_galeria = st.file_uploader("Biblioteca de Fotos do Imóvel:", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        caracteristicas = st.text_area("Características / Lista de Cômodos:", placeholder="Ex: 2 Quartos, 1 Suíte, Varanda Gourmet, 1 Vaga...")

        salvar = st.form_submit_button("💾 Salvar Dados do Imóvel", type="primary")
        if salvar:
            st.success(f"Imóvel '{endereco}' salvo com sucesso!")

# ==============================================================================
# FORMULÁRIO 2: REALIZAR VISTORIA
# ==============================================================================
elif menu == "2. Realizar Vistoria":
    st.header("🔍 Registrar Nova Vistoria")
    
    with st.form("form_vistoria"):
        # Autocompletar / Busca do Imóvel
        imovel_vistoria = st.selectbox("Selecione o Imóvel:", options=lista_enderecos, index=None, placeholder="Digite o endereço para buscar...")
        
        col1, col2 = st.columns(2)
        with col1:
            data_vistoria = st.date_input("Data da Vistoria:", datetime.today())
            vistoriador = st.text_input("Nome do Vistoriador (Usuário):")
        with col2:
            objetivo = st.text_input("Objetivo da Vistoria:", placeholder="Ex: Entrância de Inquilino, Periódica, Saída...")
            
        obs_vistoria = st.text_area("Observações Gerais da Vistoria:")
        fotos_vistoria = st.file_uploader("Anexar Fotos da Vistoria:", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
        
        st.markdown("---")
        # Sub-seção de Manutenção rápida disparada na Vistoria
        st.subheader("🛠️ Identificou necessidade de Manutenção durante a Vistoria?")
        tem_manutencao = st.checkbox("Sim, registrar apontamento de manutenção para este imóvel")
        
        if tem_manutencao:
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                servico_v = st.selectbox("Serviço Necessário:", ["Elétrica", "Hidráulica", "Infraestrutura", "Reparo", "Retirada"])
                item_v = st.selectbox("Item com Problema:", ["Quadro de Força", "Fiação", "Móveis", "Entulhos", "Outros"])
            with col_m2:
                status_v = st.selectbox("Status Inicial:", ["Identificado", "Solicitado", "Manutenção", "Concluído"])

        salvar_v = st.form_submit_button("📋 Finalizar e Salvar Vistoria", type="primary")
        if salvar_v:
            if not imovel_vistoria:
                st.error("Por favor, selecione um imóvel antes de salvar!")
            else:
                st.success(f"Vistoria salva para o imóvel: {imovel_vistoria}")

# ==============================================================================
# FORMULÁRIO 3: REGISTRO DE MANUTENÇÃO (Avulso / Painel)
# ==============================================================================
elif menu == "3. Registro de Manutenção":
    st.header("🛠️ Gestão e Atualização de Manutenções")
    
    with st.form("form_manutencao"):
        imovel_maint = st.selectbox("Selecione o Imóvel:", options=lista_enderecos, index=None, placeholder="Digite o endereço...")
        
        col1, col2 = st.columns(2)
        with col1:
            servico = st.selectbox("Tipo de Serviço:", ["Elétrica", "Hidráulica", "Infraestrutura", "Reparo", "Retirada"])
            item_afetado = st.selectbox("Item:", ["Quadro de Força", "Fiação", "Móveis", "Entulhos", "Outros"])
        with col2:
            status_maint = st.selectbox("Status Atual:", ["Identificado", "Solicitado", "Manutenção", "Concluído"])
            data_atualizacao = st.date_input("Data da Atualização:", datetime.today())
            
        detalhes_maint = st.text_area("Descrição / Detalhes do Serviço:")
        
        salvar_m = st.form_submit_button("💾 Salvar Registro de Manutenção", type="primary")
        if salvar_m:
            st.success("Registro de manutenção atualizado!")
