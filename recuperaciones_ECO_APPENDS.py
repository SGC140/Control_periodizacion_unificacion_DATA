import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.cloud import bigquery
import dotenv 
from dotenv import load_dotenv
import os
from datetime import date
import numpy as np

load_dotenv(override=True) 

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = "EFE_2026"
TABLE_ID_ORIGEN = "ECOPLUS_V2_2026"
TABLE_ID_DESTINO   = "RECUPERACIONES_ECOPLUS_2026"

Credentials_File = "credenciales.json"
client_bq = bigquery.Client.from_service_account_json(Credentials_File)

tabla_seguimiento = table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_ORIGEN}"
datos = client_bq.query(f"SELECT * FROM {tabla_seguimiento}").to_dataframe()
df = pd.DataFrame(datos)

df = df[df["novedad"] == "Activo"]

columnas_interes = ["documento", "id_sis", "gestor_asignado","novedad",
                    "programa", "ciudad", "modulo_que_cursa", "cantidad_de_modulos_cursados", 
                    "cantidad_de_modulos_aprobados"]

df = df[columnas_interes]
df["estado_aprobacion"] = np.where(df["cantidad_de_modulos_aprobados"] != df["cantidad_de_modulos_cursados"], "Con Pendientes Académicos", "Al día")

df['proyecto'] = "Ecolombia 2.0"

fecha_registro = date.today().strftime("%Y-%m-%d")
df["fecha_monitoreo"] = fecha_registro

print(df.columns.to_list())
print(df)

client_bq = bigquery.Client.from_service_account_json(Credentials_File)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID_DESTINO}"

job = client_bq.load_table_from_dataframe(
    df,
    table_ref,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        autodetect=True
    )
)

job.result()
print("Verificado")