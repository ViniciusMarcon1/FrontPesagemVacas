import requests
import pandas as pd
from datetime import datetime

BASE_URL = "http://localhost:8080/api"  

def get_pesagens():
    try:
        response = requests.get(f"{BASE_URL}/pesagens")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def get_vacas():
    try:
        response = requests.get(f"{BASE_URL}/vacas")
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def get_medidas():
    try:
        response = requests.get(f"{BASE_URL}/medidas")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def get_alertas():
    try:
        response = requests.get(f"{BASE_URL}/alertas")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['data_hora'] = pd.to_datetime(df['data_hora'])
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def get_usuarios():
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['data_criacao'] = pd.to_datetime(df['data_criacao'])
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def criar_alerta(id_vaca, tipo_alerta):
    try:
        data = {
            "id_vaca": id_vaca,
            "tipo_alerta": tipo_alerta
        }
        response = requests.post(f"{BASE_URL}/alertas", json=data)
        return response.status_code == 201
    except:
        return False 

def delete_vaca(nome):
    try:
        print(f"Trying to delete vaca: {nome}")
        response = requests.post(f"{BASE_URL}/vacas/delete", json={"nome": nome})
        print(f"Status code: {response.status_code}")
        print(f"Response body: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print("Exception in delete_vaca:", e)
        return False
