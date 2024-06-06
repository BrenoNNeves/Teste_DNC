import requests
import json
import requests
from io import BytesIO
from google.cloud import storage
import pandas as pd
import numpy as np
from google.cloud import bigquery
import matplotlib.pyplot as plt

def etl_bolsista(request):
    storage_client = storage.Client()                   
    bucket=storage_client.get_bucket("datalake-tcc") 
    
    #API retorna arquivo cvs como padrão, usei para facilitar o tratamento( em json usaria a requests)
    df=pd.read_csv('https://dados.iffarroupilha.edu.br/api/v1/bolsistas.csv', skiprows=0)
    df = df.drop_duplicates()
    df = df.dropna(how='all')

    # Padronização de formatos
    df['inicio'] = pd.to_datetime(df['inicio'], errors='coerce')
    df['fim'] = pd.to_datetime(df['fim'], errors='coerce')

    numerical_columns = ['id_tipo_bolsa', 'id_unidade_pagadora']
    df[numerical_columns] = df[numerical_columns].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Tratamento de valores nulos
    df['id_tipo_bolsa'].fillna(df['id_tipo_bolsa'].mean(), inplace=True)
    df['id_unidade_pagadora'].fillna(df['id_unidade_pagadora'].mean(), inplace=True)

    # Identificação de tendências ou padrões
    df['mes_inicio'] = df['inicio'].dt.to_period('M')
    df['mes_fim'] = df['fim'].dt.to_period('M')

    contagem_mensal_inicio = df['mes_inicio'].value_counts().sort_index()
    contagem_mensal_fim = df['mes_fim'].value_counts().sort_index()
    
    #inserir no gcp-uso a api do storage gcp
#     blob = bucket.blob('bolsistas')                 
#     blob.upload_from_string(df.to_csv(sep=',',index=False,encoding='utf-8'),content_type='application/octet-stream') 
    
    contagem_mensal_inicio.plot(kind='bar', figsize=(12, 6), title='Contagem Mensal de Início')
    plt.xlabel('Mês')
    plt.ylabel('Número de Registros')
    plt.show()

    # Visualizar contagem mensal de fim
    contagem_mensal_fim.plot(kind='bar', figsize=(12, 6), title='Contagem Mensal de Fim')
    plt.xlabel('Mês')
    plt.ylabel('Número de Registros')
    plt.show()
    return 'ok'
etl_bolsista()