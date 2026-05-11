import gspread
from google.oauth2.service_account import Credentials
from google.cloud import bigquery

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/bigquery",
]

creds = Credentials.from_service_account_file(
    "credenciales.json",
    scopes=SCOPES,
)

# Cliente para Google Sheets
gc = gspread.authorize(creds)

# Cliente para BigQuery (reutiliza las mismas credenciales)
bq = bigquery.Client(credentials=creds, project="sustained-edge-465417-m3")

# Prueba de conexión
hoja = gc.open_by_key("1GNvq_xdOfB2lBKoGzg-6ClDWGVAkfguvbIPGz4RZEqI").worksheet("SEGUIMIENTO")
print(hoja.get_all_values()[:3])  # imprime las primeras 3 filas

import pandas as pd
from google.cloud import bigquery

# ── Leer datos correctamente (2 filas de encabezado) ──────────
todos = hoja.get_all_values()

encabezados = todos[1]   # fila 2 = nombres reales de columnas
filas       = todos[2:]  # fila 3 en adelante = datos

df = pd.DataFrame(filas, columns=encabezados)

# ── Limpiar nombres de columnas ────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("\n", "_", regex=False)
    .str.replace(r"[áéíóúÁÉÍÓÚ]", lambda m: {"á":"a","é":"e","í":"i","ó":"o","ú":"u","Á":"a","É":"e","Í":"i","Ó":"o","Ú":"u"}[m.group()], regex=True)
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# Eliminar columnas sin nombre
df = df.loc[:, df.columns != ""]

# Eliminar filas completamente vacías
df = df.replace("", None).dropna(how="all")

print(f"Shape: {df.shape}")
print(df.columns.tolist())

# ── Cargar a BigQuery ──────────────────────────────────────────
BQ_PROJECT = "sustained-edge-465417-m3"
BQ_DATASET = "EFE_2026"
BQ_TABLE   = "ECOLOMBIA_2026"

tabla_ref  = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"

df = df.astype(str).replace("None", "").replace("nan", "")

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    autodetect=True,
)

job = bq.load_table_from_dataframe(df, tabla_ref, job_config=job_config)
job.result()

print(f"Cargadas {bq.get_table(tabla_ref).num_rows} filas en {tabla_ref}")