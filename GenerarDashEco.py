import os
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from google.cloud import bigquery

import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ── Configuración ──────────────────────────────────────────────
BQ_PROJECT = "sustained-edge-465417-m3"
BQ_DATASET = "EFE_2026"
BQ_TABLE   = "ECOLOMBIA_2026"

SCOPES = ["https://www.googleapis.com/auth/bigquery"]

# ── Conexión con credenciales ──────────────────────────────────
if os.environ.get("GOOGLE_CREDENTIALS"):
    creds_info = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
    creds = Credentials.from_service_account_info(creds_info, scopes=SCOPES)
else:
    creds = Credentials.from_service_account_file("credenciales.json", scopes=SCOPES)

bq = bigquery.Client(credentials=creds, project=BQ_PROJECT)

# ── Consulta ───────────────────────────────────────────────────
query = f"""
SELECT
    cohorte, grupo, programa, ciudad, etapa,
    novedad, estado_academico, estado_contratacion,
    nota_final, nota_modulo_0, nota_modulo_1,
    nota_modulo_2, nota_modulo_3, nota_modulo_4,
    nota_modulo_5, nota_modulo_6, nota_modulo_7,
    asistencias_modulo_1, asistencias_modulo_2,
    asistencias_modulo_3, asistencias_modulo_4,
    asistencias_modulo_5, asistencias_modulo_6,
    asistencias_modulo_7, asistencias_modulo_8
FROM `{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}`
"""

df = bq.query(query).to_dataframe()
print(f"Filas obtenidas: {len(df)}")

# ── Limpieza de datos ──────────────────────────────────────────
cols_notas = [c for c in df.columns if "nota" in c or "asistencia" in c]

for col in cols_notas:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", ".").str.strip(),
        errors="coerce"
    )

for col in ["cohorte", "grupo", "programa", "ciudad", "etapa", "novedad", "estado_contratacion"]:
    df[col] = df[col].fillna("Sin dato").astype(str).str.strip()

# ── App Dash ───────────────────────────────────────────────────
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Header([
        html.H1("Dashboard · EFE Colombia 2026", style={"color": "white"}),
    ], style={"background": "#1a1a2e", "padding": "1rem"}),

    html.Div([
        html.Label(["Cohorte", dcc.Dropdown(["Todos"] + sorted(df["cohorte"].unique()), "Todos", id="f-cohorte")]),
        html.Label(["Grupo", dcc.Dropdown(["Todos"] + sorted(df["grupo"].unique()), "Todos", id="f-grupo")]),
        html.Label(["Programa", dcc.Dropdown(["Todos"] + sorted(df["programa"].unique()), "Todos", id="f-programa")]),
        html.Label(["Ciudad", dcc.Dropdown(["Todos"] + sorted(df["ciudad"].unique()), "Todos", id="f-ciudad")]),
        html.Label(["Etapa", dcc.Dropdown(["Todos"] + sorted(df["etapa"].unique()), "Todos", id="f-etapa")]),
    ], style={"display": "flex", "gap": "1rem", "padding": "1rem"}),

    html.Div(id="kpis", style={"display": "grid", "gridTemplateColumns": "repeat(5, 1fr)", "gap": "1rem"}),

    html.Div([
        dcc.Graph(id="g-estado"),
        dcc.Graph(id="g-ciudad"),
        dcc.Graph(id="g-notas"),
        dcc.Graph(id="g-asistencia"),
        dcc.Graph(id="g-empleo"),
    ])
])

# ── Callback ───────────────────────────────────────────────────
@app.callback(
    Output("kpis", "children"),
    Output("g-estado", "figure"),
    Output("g-ciudad", "figure"),
    Output("g-notas", "figure"),
    Output("g-asistencia", "figure"),
    Output("g-empleo", "figure"),
    Input("f-cohorte", "value"),
    Input("f-grupo", "value"),
    Input("f-programa", "value"),
    Input("f-ciudad", "value"),
    Input("f-etapa", "value"),
)
def actualizar(cohorte, grupo, programa, ciudad, etapa):
    d = df.copy()

    if cohorte != "Todos": d = d[d["cohorte"] == cohorte]
    if grupo != "Todos": d = d[d["grupo"] == grupo]
    if programa != "Todos": d = d[d["programa"] == programa]
    if ciudad != "Todos": d = d[d["ciudad"] == ciudad]
    if etapa != "Todos": d = d[d["etapa"] == etapa]

    total = len(d)
    activos = int((d["novedad"] == "Activo").sum())
    desertores = int(d["novedad"].str.contains("eser", case=False, na=False).sum())
    contratados = int(d["estado_contratacion"].str.contains("ontrat", case=False, na=False).sum())
    retencion = f"{round(activos/total*100) if total else 0}%"

    def kpi(label, valor):
        return html.Div([
            html.H4(label),
            html.H2(valor)
        ], style={"background": "white", "padding": "10px", "borderRadius": "8px"})

    kpis = [
        kpi("Total", total),
        kpi("Activos", activos),
        kpi("Desertores", desertores),
        kpi("Contratados", contratados),
        kpi("Retención", retencion),
    ]

    fig_estado = px.pie(d, names="novedad", title="Estado")
    fig_ciudad = px.bar(d["ciudad"].value_counts().head(10), title="Ciudades")
    fig_notas = px.bar(x=[f"M{i}" for i in range(8)],
                       y=[d[f"nota_modulo_{i}"].mean() for i in range(8)],
                       title="Notas")
    fig_asistencia = px.line(x=[f"M{i}" for i in range(1, 9)],
                             y=[d[f"asistencias_modulo_{i}"].mean() for i in range(1, 9)],
                             title="Asistencia")
    fig_empleo = px.bar(d["estado_contratacion"].value_counts(), title="Empleo")

    return kpis, fig_estado, fig_ciudad, fig_notas, fig_asistencia, fig_empleo

# ── Run ────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)