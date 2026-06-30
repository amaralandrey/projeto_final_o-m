import re
import pandas as pd

def extrair_padroes_coluna(series):
    """
    Analisa os valores de uma coluna (Pandas Series) para identificar
    se correspondem a padrões de CPF, Email, Telefone ou Nome Completo.
    """
    valores = series.dropna().astype(str).str.strip()
    
    if valores.empty:
        return None

    # 1. Expressões Regulares (Regex)
    regex_cpf = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'
    regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    regex_telefone = r'^\(?[1-9]{2}\)? ?(?:[2-8]|9[1-9])\d{3}-?\d{4}$'
    
    # Regex para Nome Completo: Pelo menos Nome + Sobrenome, aceitando acentos e preposições
    regex_nome = r'^[A-ZÀ-Ú][a-zà-úçéèíóôõúü\s]+(?:\s+[A-ZÀ-Ú][a-zà-úçéèíóôõúü\s]+)+$'

    amostra = valores.head(50)
    total_itens = len(amostra)
    
    cpfs_encontrados = sum(1 for v in amostra if re.match(regex_cpf, v))
    emails_encontrados = sum(1 for v in amostra if re.match(regex_email, v))
    telefones_encontrados = sum(1 for v in amostra if re.match(regex_telefone, v))
    nomes_encontrados = sum(1 for v in amostra if re.match(regex_nome, v))

    # Classificação baseada no limiar de 70%
    if cpfs_encontrados / total_itens > 0.7:
        return "CPF"
    elif emails_encontrados / total_itens > 0.7:
        return "E-mail"
    elif telefones_encontrados / total_itens > 0.7:
        return "Telefone"
    elif nomes_encontrados / total_itens > 0.7:
        return "Nome Completo"
        
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
