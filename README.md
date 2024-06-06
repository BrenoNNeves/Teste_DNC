### README

## Prévia

Não consegui entregar com alta qualidade devida ao pouco tempo que tive, porém me garanto nas habilidades exigidas, já passei por 3 grandes empresas atuei em mais de 3 projetos de dados diferentes utilizando Python, Sql, CI/CD, Airflow, DBT, SnowFlake, GCP, AWS e entre outras tecnologias, utilizei como base o meu TCC em que fiz todo o ETL e arquitetura de um Data Mesh e um DataLake e os comparei, entendo os conceitos de clen code e segurança de chaves, caso queiram uma entrevista tecnica estou a disposição.


## Projeto: Gerenciamento de Bolsas Acadêmicas

Este projeto visa o gerenciamento de dados relacionados a bolsas acadêmicas, incluindo informações sobre discentes, cursos, tipos de bolsa e unidades pagadoras. Este documento fornece uma explicação detalhada das etapas necessárias para preparar e armazenar os dados em um banco de dados relacional.

### Sumário

1. [Estrutura dos Dados](#estrutura-dos-dados)
2. [Pré-processamento dos Dados](#pré-processamento-dos-dados)
3. [Esquema de Banco de Dados](#esquema-de-banco-de-dados)
4. [Definição SQL do Esquema](#definição-sql-do-esquema)
5. [Execução do Código](#execução-do-código)
6. [Visualização de Tendências](#visualização-de-tendências)

### Estrutura dos Dados

A planilha extraida da API fornecida contém as seguintes colunas:

- `id`: Identificador único da bolsa.
- `matricula`: Número de matrícula do discente.
- `id_discente`: Identificador único do discente.
- `id_curso_sigaa`: Identificador único do curso.
- `id_tipo_bolsa`: Identificador do tipo de bolsa.
- `inicio`: Data de início da bolsa.
- `fim`: Data de fim da bolsa.
- `id_unidade_pagadora`: Identificador da unidade pagadora.

### Pré-processamento dos Dados

O pré-processamento dos dados envolve as seguintes etapas:

1. **Remoção de duplicatas e registros inválidos**:
    - Remover linhas duplicadas.
    - Remover linhas onde todas as colunas são `None`.

2. **Padronização de formatos**:
    - Converter colunas de datas (`inicio` e `fim`) para o formato datetime.
    - Converter colunas numéricas (`id_tipo_bolsa` e `id_unidade_pagadora`) para o formato numérico, preenchendo valores nulos com zero.

3. **Tratamento de valores nulos**:
    - Preencher valores nulos nas colunas `id_tipo_bolsa` e `id_unidade_pagadora` com a média das respectivas colunas.

4. **Identificação de tendências**:
    - Calcular a contagem de registros por mês de início e fim das bolsas.

### Esquema de Banco de Dados

Para armazenar os dados, definimos um esquema de banco de dados relacional com as seguintes tabelas:

1. **Tabela `discentes`**:
    - `id_discente`: Chave primária.
    - `matricula`: Número de matrícula do discente.

2. **Tabela `cursos`**:
    - `id_curso_sigaa`: Chave primária.
    - `nome_curso`: Nome do curso (adicionado para melhor estrutura).

3. **Tabela `tipos_bolsa`**:
    - `id_tipo_bolsa`: Chave primária.
    - `descricao_bolsa`: Descrição da bolsa (adicionado para melhor estrutura).

4. **Tabela `unidades_pagadoras`**:
    - `id_unidade_pagadora`: Chave primária.
    - `nome_unidade`: Nome da unidade pagadora (adicionado para melhor estrutura).

5. **Tabela `bolsas`**:
    - `id`: Chave primária.
    - `id_discente`: Chave estrangeira referenciando `discentes(id_discente)`.
    - `id_curso_sigaa`: Chave estrangeira referenciando `cursos(id_curso_sigaa)`.
    - `id_tipo_bolsa`: Chave estrangeira referenciando `tipos_bolsa(id_tipo_bolsa)`.
    - `inicio`: Data de início da bolsa.
    - `fim`: Data de fim da bolsa.
    - `id_unidade_pagadora`: Chave estrangeira referenciando `unidades_pagadoras(id_unidade_pagadora)`.

### Definição SQL do Esquema

```sql
CREATE TABLE discentes (
    id_discente INT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL
);

CREATE TABLE cursos (
    id_curso_sigaa INT PRIMARY KEY,
    nome_curso VARCHAR(255)
);

CREATE TABLE tipos_bolsa (
    id_tipo_bolsa INT PRIMARY KEY,
    descricao_bolsa VARCHAR(255)
);

CREATE TABLE unidades_pagadoras (
    id_unidade_pagadora INT PRIMARY KEY,
    nome_unidade VARCHAR(255)
);

CREATE TABLE bolsas (
    id INT PRIMARY KEY,
    id_discente INT,
    id_curso_sigaa INT,
    id_tipo_bolsa INT,
    inicio DATE,
    fim DATE,
    id_unidade_pagadora INT,
    FOREIGN KEY (id_discente) REFERENCES discentes(id_discente),
    FOREIGN KEY (id_curso_sigaa) REFERENCES cursos(id_curso_sigaa),
    FOREIGN KEY (id_tipo_bolsa) REFERENCES tipos_bolsa(id_tipo_bolsa),
    FOREIGN KEY (id_unidade_pagadora) REFERENCES unidades_pagadoras(id_unidade_pagadora)
);
```

### Execução do Código

Para executar o código de pré-processamento e análise de tendências, siga os passos abaixo:

1. **Carregar a planilha**:

```python
import pandas as pd

file_path = '/mnt/data/data.csv'
df = pd.read_csv(file_path)
```

2. **Remover duplicatas e registros inválidos**:

```python
df = df.drop_duplicates()
df = df.dropna(how='all')
```

3. **Padronizar formatos**:

```python
df['inicio'] = pd.to_datetime(df['inicio'], errors='coerce')
df['fim'] = pd.to_datetime(df['fim'], errors='coerce')

numerical_columns = ['id_tipo_bolsa', 'id_unidade_pagadora']
df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce').fillna(0)
```

4. **Tratar valores nulos**:

```python
df['id_tipo_bolsa'].fillna(df['id_tipo_bolsa'].mean(), inplace=True)
df['id_unidade_pagadora'].fillna(df['id_unidade_pagadora'].mean(), inplace=True)
```

5. **Identificar tendências**:

```python
df['mes_inicio'] = df['inicio'].dt.to_period('M')
df['mes_fim'] = df['fim'].dt.to_period('M')

contagem_mensal_inicio = df['mes_inicio'].value_counts().sort_index()
contagem_mensal_fim = df['mes_fim'].value_counts().sort_index()
```

### Visualização de Tendências

Para visualizar as tendências mensais de registros de início e fim:

```python
import matplotlib.pyplot as plt

# Visualizar contagem mensal de início
contagem_mensal_inicio.plot(kind='bar', figsize=(12, 6), title='Contagem Mensal de Início')
plt.xlabel('Mês')
plt.ylabel('Número de Registros')
plt.show()

# Visualizar contagem mensal de fim
contagem_mensal_fim.plot(kind='bar', figsize=(12, 6), title='Contagem Mensal de Fim')
plt.xlabel('Mês')
plt.ylabel('Número de Registros')
plt.show()
```

### Conclusão

Este projeto fornece uma estrutura organizada para o gerenciamento de dados de bolsas acadêmicas, com etapas claras para o pré-processamento de dados, definição de esquema de banco de dados e visualização de tendências. Se precisar de mais alguma análise ou tiver alguma dúvida, sinta-se à vontade para perguntar!