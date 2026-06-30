import os
import sys
import streamlit as st
import pandas as pd
import spacy

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Scanner LGPD - PMEs", 
    page_icon="🛡️", 
    layout="centered"
)

# --- INICIALIZAÇÃO DO NLP À PROVA DE FALHAS ---
@st.cache_resource
def carregar_modelo_nlp():
    """
    Tenta carregar por string. Se falhar, executa o download usando o pip 
    do próprio ambiente virtual ativo e recarrega o sys.path.
    """
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        with st.spinner("📥 Configurando o motor de inteligência em português para o primeiro uso... Aguarde alguns segundos."):
            # Roda o download apontando exatamente para o executável do Python ativo
            os.system(f"{sys.executable} -m spacy download pt_core_news_sm")
            # Força o recarregamento interno do spaCy
            return spacy.load("pt_core_news_sm")

# Carrega o modelo com segurança (se falhar na primeira, ele baixa e tenta de novo)
try:
    nlp = carregar_modelo_nlp()
except Exception as e:
    st.error(f"Erro ao inicializar o motor de buscas (NLP): {e}")
    st.info("Por favor, tente reiniciar o aplicativo no painel do Streamlit.")
    st.stop()

# --- IMPORTAÇÕES DO PROJETO ---
# (Mova suas importações para DEPOIS do carregamento do NLP para evitar quebras)
from motor_busca import analisar_dataframe
from gerador_pdf import gerar_pdf_bytes

# --- INTERFACE VISUAL ---
st.title("🛡️ Scanner de Conformidade LGPD")
st.subheader("Inventário Automatizado para Pequenas e Médias Empresas")

st.markdown("""
Faça o upload de arquivos estruturados (**CSV** ou **XLSX**) para identificar automaticamente a presença 
de dados pessoais (CPF, E-mail, Telefone, Nome Completo) e gerar o relatório de riscos sem salvar nenhuma informação no servidor.
""")

# Componente de Upload de Arquivos
arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        # 1. Ingestão e Processamento 100% em Memória
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)
            
        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        
        # 2. Execução do Motor de Busca
        st.write("### 🔍 Analisando dados...")
        resultados = analisar_dataframe(df)
        
        # 3. Exibição do Diagnóstico e Nível de Risco na Tela
        if resultados:
            st.warning("⚠️ Foram encontrados dados pessoais no arquivo!")
            dados_tabela = [{"Coluna no Arquivo": col, "Tipo de Dado Detectado": tipo} for col, tipo in resultados.items()]
            st.table(dados_tabela)
            
            qtd_colunas_expostas = len(resultados)
            if qtd_colunas_expostas >= 3:
                st.error("🚨 Nível de Risco Geral: ALTO (Múltiplos identificadores expostos)")
            else:
                st.warning("⚠️ Nível de Risco Geral: MÉDIO (Dados pessoais identificados)")
        else:
            # Caso não encontre nada, exibe sucesso na tela
            st.success("✅ Nenhum dado pessoal evidente (CPF, Email, Telefone, Nome Completo) foi detectado nas amostras.")
            
        # 4. Geração e Download do Relatório em PDF
        st.write("---")
        st.write("### 📄 Relatório de Adequação")
        st.markdown("Clique no botão abaixo para descarregar o relatório oficial de riscos da LGPD em formato PDF.")
        
        pdf_data = gerar_pdf_bytes(resultados, len(df))
        
        st.download_button(
            label="📥 Descarregar Relatório PDF",
            data=bytes(pdf_data),
            file_name=f"Relatorio_Adequacao_LGPD_{arquivo.name}.pdf",
            mime="application/pdf"
        )
            
        # 5. Pré-visualização dos Dados Originais (Apenas as primeiras 5 linhas)
        st.write("---")
        st.write("#### Pré-visualização dos dados enviados:")
        st.dataframe(df.head(5))
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
