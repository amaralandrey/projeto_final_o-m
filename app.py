import streamlit as st
import pandas as pd
# Importamos a função que acabamos de criar no outro arquivo
from motor_busca import analisar_dataframe

st.set_page_config(page_title="Scanner LGPD", page_icon="🛡️", layout="centered")

st.title("🛡️ Scanner de Conformidade LGPD")
st.subheader("Inventário Automatizado para PMEs")

st.markdown("Faça o upload de arquivos estruturados (CSV ou XLSX) para identificar automaticamente a presença de dados pessoais.")

arquivo = st.file_uploader("Selecione o arquivo de dados", type=["csv", "xlsx"])

if arquivo is not None:
    try:
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)
            
        st.success(f"Arquivo '{arquivo.name}' carregado com sucesso!")
        
        # --- AQUI ENTRA O NOSSO MOTOR DE BUSCA ---
        st.write("### 🔍 Analisando dados...")
        
        # Executa a análise na memória
        resultados = analisar_dataframe(df)
        
        if resultados:
            st.warning("⚠️ Foram encontrados dados pessoais no arquivo!")
            
            # Mostra os resultados em formato de tabela simples
            dados_tabela = [{"Coluna no Arquivo": col, "Tipo de Dado Detectado": tipo} for col, tipo in resultados.items()]
            st.table(dados_tabela)
            
            # Cálculo simples de risco para o MVP
            qtd_colunas_expostas = len(resultados)
            if qtd_colunas_expostas >= 3:
                st.error("🚨 Nível de Risco Geral: ALTO (Múltiplos identificadores sensíveis expostos)")
            else:
                st.warning("⚠️ Nível de Risco Geral: MÉDIO (Dados pessoais identificados)")
        else:
            st.success("✅ Nenhum dado pessoal evidente (CPF, Email, Telefone) foi detectado nas amostras.")
            
        # Exibe os dados originais abaixo do diagnóstico
        st.write("---")
        st.write("#### Pré-visualização dos dados enviados:")
        st.dataframe(df.head(5))
        
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
