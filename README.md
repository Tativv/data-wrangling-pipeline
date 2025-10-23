# 📊 Pipeline de Vendas

Script em Python que realiza extração, transformação e carga (ETL) de dados de vendas, criando um banco SQLite **(vendas.db)** pronto para consultas.

# ⚙️ Pré-requisitos
Python 3.10+

Bibliotecas do requirements.txt:
```
pip install -r requirements.txt
```

# ▶️ Como rodar

## Pelo terminal (bash/powershell)
1. Coloque o arquivo vendas.csv na pasta correta ou ajuste o caminho no código.
2. No terminal, execute:
```
pippython src/pipeline.py
```
## Diretamente no VS Code

1. Abra o projeto no VS Code.

2. Certifique-se de que Python 3.10+ esteja selecionado como interpretador (canto inferior direito).

3. Abra src/pipeline.py.

4. Clique no botão Run (▶️) no canto superior direito ou pressione F5.

O script será executado no Terminal integrado, mostrando todas as etapas do pipeline.

💡 Dica: usar a extensão Code Runner permite executar arquivos Python rapidamente clicando com o botão direito → Run Code.

# 📌 O que o script faz

📥 Carregar e explorar os dados

🧹 Limpar e padronizar datas, valores nulos, quantidades e preços

➕ Criar coluna valor_total

💾 Criar banco SQLite com tabelas tb_clientes e tb_vendas

📊 Gerar resumo de vendas por categoria

# 👥 Equipe
## Nina da Hora
