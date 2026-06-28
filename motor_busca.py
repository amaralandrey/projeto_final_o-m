import re
import pandas as pd

def extrair_padroes_coluna(series):
    """
    Analisa os valores de uma coluna (Pandas Series) para identificar
    se correspondem a padrões de CPF, Email ou Telefone.
    """
    # Convertemos todos os valores para string e removemos espaços em branco
    valores = series.dropna().astype(str).str.strip()
    
    if valores.empty:
        return None

    # 1. Expressões Regulares (Regex) para cada tipo de dado
    regex_cpf = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    # Aceita formatos: (XX) 9XXXX-XXXX, XX9XXXXXXXX, etc.
    regex_telefone = r'^?\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])\d{3}-?\d{4}$'

    # Vamos testar o padrão nas primeiras 50 linhas para classificar a coluna
    amostra = valores.head(50)
    
    total_itens = len(amostra)
    cpfs_encontrados = sum(1 for v in amostra if re.match(regex_cpf, v))
    emails_encontrados = sum(1 for v in amostra if re.match(regex_email, v))
    telefones_encontrados = sum(1 for v in amostra if re.match(regex_telefone, v))

    # Se mais de 70% da amostra bater com o padrão, classificamos a coluna
    if cpfs_encontrados / total_itens > 0.7:
        return "CPF"
    elif emails_encontrados / total_itens > 0.7:
        return "E-mail"
    elif telefones_encontrados / total_itens > 0.7:
        return "Telefone"
        
    return None

def analisar_dataframe(df):
    """
    Varre todo o DataFrame coluna por coluna e retorna um inventário
    de onde foram encontrados dados pessoais.
    """
    inventario = {}
    
    for coluna in df.columns:
        tipo_dado = extrair_padroes_coluna(df[coluna])
        if tipo_dado:
            inventario[coluna] = tipo_dado
            
    return inventario
