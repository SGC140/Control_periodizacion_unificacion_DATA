import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from google.cloud import bigquery
import dotenv 
from dotenv import load_dotenv
import os

load_dotenv()
load_dotenv(override=True)
SEGUIMIENTO_STC = os.getenv("Sheets_FCS_STC_3_0")

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = "EFE_2026"
TABLE_ID   = "STC_3_0_FCS_2026"

Credentials_File = "credenciales.json"

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(Credentials_File, scopes=scopes)
client_sheets = gspread.authorize(creds)

sheet = client_sheets.open_by_key(SEGUIMIENTO_STC)
Hoja_FCS = sheet.worksheet("CONSOLIDADO")
Datos = Hoja_FCS.get_all_values()
DF = pd.DataFrame(Datos[6:], columns=Datos[5])
Headers = DF.columns
DF = DF.loc[:, DF.columns != ""]

DF = DF.replace(r'^\s*$', None, regex=True)
DF = DF.where(pd.notnull(DF), None)
DF = DF.dropna(subset=['NÚMERO DE DOCUMENTO'])

Columnas_numericas = ['EDAD']

DF[Columnas_numericas] = DF[Columnas_numericas].replace(",", ".", regex=True) 
DF[Columnas_numericas] = DF[Columnas_numericas].apply(pd.to_numeric, errors = 'coerce')

#Columnas_fecha = [columna for columna in DF.columns if 'fecha' in columna.lower().strip()]
#DF[Columnas_fecha] = DF[Columnas_fecha].apply(pd.to_datetime, errors='coerce')
#DF[Columnas_fecha] = DF[Columnas_fecha].apply(lambda x: x.dt.strftime('%d/%m/%Y'))

DF.columns = DF.columns.str.strip()
DF.columns = (DF.columns
              .str.replace(" ","_")
              .str.normalize('NFKD')
              .str.encode('ascii', errors='ignore')
              .str.decode('utf-8')
              .str.lower()
              .str.replace(r"[\r\n]+", "", regex=True)
              .str.replace(r"[^a-z0-9_#_.]", "", regex=True)              
              )

DF = DF.loc[:, ~DF.columns.duplicated()]

DF['proyecto'] = "Socios Talento Capital 3.0"

print(DF.columns.to_list())


client_bq = bigquery.Client.from_service_account_json(Credentials_File)
table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

from validacion_dataframes import validar_y_comparar
validar_y_comparar(Hoja_FCS.title, DF, client_bq, table_ref)

job = client_bq.load_table_from_dataframe(
    DF,
    table_ref,
    job_config=bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
)

job.result()
print("Verificado")