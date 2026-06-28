import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scanner", page_icon="🛡️", layout="centered")
st.title("🛡️ Scanner")
st.subheader("Inventário Automatizado")
st.markdown("Faça o upload de arquivos estruturados (CSV ou XLSX) para identificar
automaticamente a presença de dados pessoais.")
arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])
if arquivo is not None:
    try:
        if arquivo.name.endswith('.csv'):
        df = pd.read_csv(arquivo)

        else:
            df = pd.read_excel(arquivo)

        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        st.info(f"O arquivo possui {df.shape[0]} linhas e {df.shape[1]} colunas.")
        st.dataframe(df.head(5))

        if st.button("Simular Geração de Relatório PDF"):
            st.warning("O motor de busca e o gerador de PDF serão integrados na próxima etapa.")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
