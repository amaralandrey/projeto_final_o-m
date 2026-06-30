# Proposta
Nossa proposta é uma plataforma de descoberta e inventário automatizado de dados pessoais para apoio à conformidade com a LGPD em pequenas e médias empresas.

## Escopo do MVP
- Scanner para arquivos estruturados (CSV/XLSX) locais.
- Identificação automática de dados pessoais (CPF, nome, email, telefone, endereço).
- Classificação de risco.
- Geração de relatório de adequação a LGPD em PDF.

## Arquitetura
#### Back end
- Python
  
#### Front end
- Streamlit

## Fluxo do usuário 
- Usuário faz upload de arquivo: CSV, XLSX  
- Sistema analisa colunas  
- Sistema calcula risco  
- Sistema gera relatório com recomendações
