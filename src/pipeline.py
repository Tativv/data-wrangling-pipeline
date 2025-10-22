import pandas as pd
from datetime import datetime
import sqlite3
from colorama import Fore, Style, init

init(autoreset=True)

# ==============================
# EXTRAÇÃO DE DADOS
# ==============================

print(Fore.CYAN + '\nEtapa 1: Extraindo dados...\n')
df_vendas = pd.read_csv("dataset/vendas.csv")
print(df_vendas.head())

# ==============================
# PADRONIZAÇÃO E LIMPEZA
# ==============================

#  Padronizar a coluna de data (YYYY-MM-DD)
print(Fore.GREEN + '\nPadronizar a coluna de data (YYYY-MM-DD)......\n')
def normalizando_data(date_str):
    date_str = str(date_str).replace("/", "-")
    formatos = ["%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y"]
    for formato in formatos:
        try:
            return datetime.strptime(date_str, formato)
        except ValueError:
            pass
    return pd.NaT

df_vendas['data_venda'] = df_vendas['data_venda'].apply(normalizando_data)
df_vendas['data_venda'] = df_vendas['data_venda'].dt.strftime('%Y-%m-%d')
print(df_vendas.head())

# Valores nulos e correção de quantidade
print( Fore.GREEN + '\nSubstituindo valores nulos por "Não informado".....')
df_vendas = df_vendas.fillna("Não informado")

print( Fore.GREEN + '\nCorrigindo quantidade para ser sempre número inteiro......') 
df_vendas['quantidade'] = df_vendas['quantidade'].replace('três', '3').astype(int)

# Preços negativos
print( Fore.GREEN + '\nRemovendo preços negativos......') 
df_vendas = df_vendas[df_vendas['preco_unitario'] >= 0]

# Criar coluna valor_total
print( Fore.GREEN + '\nCriando uma nova coluna valor_total.....\n')
df_vendas["valor_total"] = df_vendas["quantidade"] * df_vendas["preco_unitario"]
print(df_vendas.head())

# ==============================
# CRIAÇÃO DO BANCO DE DADOS
# ==============================

print( Fore.YELLOW + '\nCriando um banco SQLite (arquivo vendas.db).........')
conexao = sqlite3.connect("vendas.db")
cursor = conexao.cursor()
cursor.execute("PRAGMA foreign_keys = ON;") 

# Criar tabela de clientes únicos
print( Fore.YELLOW + '\nCriando tabela tb_clientes contendo apenas clientes únicos.....\n')
tb_clientes = df_vendas[['cliente']].drop_duplicates().reset_index(drop=True)
tb_clientes['cliente_id'] = tb_clientes.index + 1
print(tb_clientes)

print( Fore.YELLOW + '\nCombinando DataFrames.....\n')
df = df_vendas.merge(tb_clientes, on='cliente', how='left')
print(df.head())

# Criar tabelas no SQLite
print( Fore.YELLOW + '\nRelacionando tb_vendas com tb_clientes via chave estrangeira ......')
cursor.execute("""
CREATE TABLE IF NOT EXISTS tb_clientes (
    cliente_id INTEGER PRIMARY KEY,
    cliente TEXT
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tb_vendas (
    id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data_venda TEXT,
    produto TEXT,
    quantidade INTEGER,
    preco_unitario REAL,
    valor_total REAL,
    categoria TEXT,
    FOREIGN KEY (cliente_id) REFERENCES tb_clientes(cliente_id)
);
""")

tb_clientes.to_sql("tb_clientes", conexao, if_exists="replace", index=False)
df.to_sql("tb_vendas", conexao, if_exists="replace", index=False)

# ==============================
# CONSULTA SQL
# ==============================

print( Fore.MAGENTA + '\n====== Consulta SQL ======')
query_total_por_categoria = """
SELECT categoria, SUM(valor_total) AS total_vendas
FROM tb_vendas
GROUP BY categoria
ORDER BY total_vendas DESC;
"""
df_total_por_categoria = pd.read_sql_query(query_total_por_categoria, conexao)
print(df_total_por_categoria)

# Fechar conexão
conexao.close()
print(Fore.RED + "\nConexão fechada com sucesso!")