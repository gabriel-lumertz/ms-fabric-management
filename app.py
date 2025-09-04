import requests
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from auth import get_token

load_dotenv()


def main():
    token = get_token()

    URL = "https://api.powerbi.com/v1.0/myorg/admin/groups?$top=500&$expand=users"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Normaliza o JSON principal
    df = pd.json_normalize(
        data.get("value", []),
        sep='.'
    )

    # Expande a coluna 'users' em linhas separadas
    if 'users' in df.columns:
        df = df.explode('users').reset_index(drop=True)
        # Expande os campos do dicionário de users em colunas
        users_df = pd.json_normalize(df['users'])
        # Remove a coluna antiga e concatena as novas colunas
        df = df.drop(columns=['users']).reset_index(drop=True)
        df = pd.concat([df, users_df], axis=1)

    # Mantém apenas as colunas desejadas
    colunas_desejadas = ['id', 'name', 'emailAddress', 'displayName']
    df = df[[col for col in colunas_desejadas if col in df.columns]]

    st.set_page_config(page_title="Power BI Admin Groups", layout="wide")
    st.title("Tabela de Workspaces do Power BI")
    st.dataframe(df)


if __name__ == "__main__":
    main()
