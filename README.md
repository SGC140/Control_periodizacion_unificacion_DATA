# Data Ingestion and Management Pipeline

Este repositorio alberga una colección de scripts diseñados para la ingesta, transformación y gestión de datos provenientes de diversas fuentes operacionales (principalmente Google Sheets) hacia un Data Warehouse centralizado en Google BigQuery. El sistema automatiza la limpieza, validación y carga de datos para múltiples proyectos, asegurando la consistencia y disponibilidad de la información para análisis y reportes.

---

## Badges

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-BigQuery-orange?style=for-the-badge&logo=google-cloud)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-API-green?style=for-the-badge&logo=google-sheets)
![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-red?style=for-the-badge&logo=pandas)
![Project Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

---

## Índice

1.  [Visión General del Proyecto](#1-visión-general-del-proyecto)
2.  [Arquitectura del Sistema](#2-arquitectura-del-sistema)
    *   [Flujo de Datos](#21-flujo-de-datos)
    *   [Componentes Principales](#22-componentes-principales)
3.  [Estructura del Repositorio](#3-estructura-del-repositorio)
4.  [Configuración del Entorno](#4-configuración-del-entorno)
    *   [Dependencias a Nivel de Sistema Operativo](#41-dependencias-a-nivel-de-sistema-operativo)
    *   [Dependencias de Python](#42-dependencias-de-python)
    *   [Variables de Entorno](#43-variables-de-entorno)
    *   [Autenticación de Google Cloud](#44-autenticación-de-google-cloud)
5.  [Lógica Principal y Pipeline](#5-lógica-principal-y-pipeline)
    *   [Scripts de Ingestión de Datos (Upload)](#51-scripts-de-ingestión-de-datos-upload)
    *   [Módulo de Validación de Esquemas (`validacion_dataframes.py`)](#52-módulo-de-validación-de-esquemas-validacion_dataframespy)
    *   [Script de Apéndice Histórico (`Append_DATA_BQ.py`)](#53-script-de-apéndice-histórico-append_data_bqpy)
    *   [Scripts de Perfilado de Datos (`Limpieza_*.py`)](#54-scripts-de-perfilado-de-datos-limpieza_py)
    *   [Orquestador de Ejecución (`trigger.py`)](#55-orquestador-de-ejecución-triggerpy)
6.  [Ejemplos de Salida de Datos](#6-ejemplos-de-salida-de-datos)
    *   [DataFrame Limpio (Previo a BigQuery)](#61-dataframe-limpio-previo-a-bigquery)
    *   [Tabla de Apéndice Histórico en BigQuery](#62-tabla-de-apéndice-histórico-en-bigquery)
7.  [Valor de Negocio y Capacidades Analíticas](#7-valor-de-negocio-y-capacidades-analíticas)
    *   [Lo que se Muestra](#71-lo-que-se-muestra)
    *   [Lo que Permite Medir](#72-lo-que-permite-medir)
    *   [Lo que Permite Diagnosticar](#73-lo-que-permite-diagnosticar)
    *   [Lo que Permite Resolver](#74-lo-que-permite-resolver)
    *   [Lo que Permite Acotar](#75-lo-que-permite-acotar)
    *   [Lo que Permite Optimizar](#76-lo-que-permite-optimizar)
    *   [Lo que Permite Estandarizar](#77-lo-que-permite-estandarizar)
    *   [Lo que Permite Repensar](#78-lo-que-permite-repensar)

---

## 1. Visión General del Proyecto

Este proyecto automatiza la extracción, transformación y carga (ETL) de datos desde Google Sheets hacia Google BigQuery. Su objetivo principal es consolidar información operativa de múltiples programas y proyectos (e.g., "Ecolombia 2.0", "Colsubsidio 2026", "Jóvenes a la E", "Suba es Oportunidad") en un formato estructurado y centralizado. Esto facilita el análisis de datos, la generación de informes y la toma de decisiones basada en evidencia, eliminando la dependencia de procesos manuales propensos a errores y lentos.

---

## 2. Arquitectura del Sistema

La arquitectura se basa en un enfoque de micro-servicios (scripts) que interactúan con APIs de Google Cloud y bibliotecas de procesamiento de datos.

### 2.1 Flujo de Datos

El pipeline de datos sigue un patrón claro:

1.  **Origen**: Datos operativos residen en hojas de cálculo de Google Sheets, gestionadas por diferentes equipos de proyecto.
2.  **Extracción**: Los scripts de Python utilizan la API de Google Sheets (`gspread`) para leer los datos.
3.  **Transformación**: `pandas` se emplea para realizar operaciones de limpieza, normalización de nombres de columnas, conversión de tipos de datos, manejo de valores nulos y eliminación de duplicados.
4.  **Validación**: Un módulo de validación de esquemas compara la estructura del DataFrame transformado con el esquema de la tabla de destino en BigQuery para prevenir inconsistencias.
5.  **Carga**: Los datos limpios y validados se cargan en tablas específicas de Google BigQuery (`google-cloud-bigquery`).
6.  **Orquestación**: Un script `trigger.py` coordina la ejecución de todos los scripts de ingesta.
7.  **Apéndice Histórico**: Un script dedicado (`Append_DATA_BQ.py`) gestiona la creación de instantáneas históricas de ciertas tablas en BigQuery.
8.  **Perfilado de Datos**: Scripts de limpieza (`Limpieza_*.py`) permiten inspeccionar la calidad de los datos ya cargados en BigQuery.

### 2.2 Componentes Principales

*   **Google Sheets**: Fuente de datos primarios.
*   **Google Cloud BigQuery**: Data Warehouse escalable y sin servidor para el almacenamiento y análisis de datos.
*   **Python Scripts**:
    *   **Scripts de Ingestión (`Upload_*.py`, `Caracterizacion_*.py`, `Empleabilidad_*.py`, `Satisfaccion_*.py`, `CONVOCATORIA_*.py`, `UnificadoFormacion_*.py`)**: Responsables de la extracción, limpieza y carga de datos para cada fuente específica.
    *   **`validacion_dataframes.py`**: Módulo de control de calidad de esquemas.
    *   **`Append_DATA_BQ.py`**: Gestiona la creación de tablas históricas.
    *   **`Limpieza_*.py`**: Scripts de perfilado de datos para BigQuery.
    *   **`trigger.py`**: Orquestador principal del pipeline de ingesta.
*   **`credenciales.json`**: Archivo de credenciales de cuenta de servicio para autenticación en Google Cloud.
*   **`.env`**: Archivo para la gestión segura de variables de entorno (IDs de proyectos, datasets, hojas de cálculo).

---

## 3. Estructura del Repositorio

```
.
├── Append_DATA_BQ.py
├── CONVOCATORIA_ECOLOMBIA_2026.py
├── Caracterizacion Colsubsidio2026.py
├── Caracterizacion_ECO_2026.py
├── Caracterizacion_JAE_2026.py
├── Caracterizacion_Suba2026.py
├── Empleabilidad_ECO.py
├── Empleabilidad_JAE_2026_V1.0.py
├── Empleabilidad_Suba2026.py
├── Limpieza_caracterizacion.py
├── Limpieza_empleabilidad.py
├── Limpieza_satisfaccion.py
├── Limpieza_seguimiento.py
├── Satisfaccion_Colsubsidio2026.py
├── Satisfaccion_ECO.py
├── Satisfaccion_JAE_2026.py
├── Satisfaccion_Suba.py
├── UnificadoFormacion_Suba2026.py
├── Upload Colsubsidio2026.py
├── Upload Suba2026.py
├── Upload_ECO++_2026.py
├── Upload_JAE_2026.py
├── trigger.py
├── validacion_dataframes.py
├── credenciales.json
└── .env
```

---

## 4. Configuración del Entorno

Para ejecutar los scripts, es necesario configurar el entorno de desarrollo y autenticación.

### 4.1 Dependencias a Nivel de Sistema Operativo

Este proyecto no requiere dependencias específicas a nivel de sistema operativo más allá de una instalación estándar de Python. Todas las bibliotecas necesarias se gestionan a través de `pip`.

### 4.2 Dependencias de Python

Las bibliotecas de Python requeridas se listan a continuación. Se recomienda usar un entorno virtual para su instalación.

```bash
pip install pandas gspread google-cloud-bigquery python-dotenv
```

### 4.3 Variables de Entorno

Se utiliza un archivo `.env` para gestionar variables de entorno sensibles y configuraciones específicas del proyecto. Este archivo **no debe ser versionado** en sistemas de control de código fuente.

Cree un archivo `.env` en la raíz del proyecto con el siguiente formato, reemplazando los valores de ejemplo con los suyos:

```dotenv
PROJECT_ID="your-gcp-project-id"
DATA_SET="your-bigquery-dataset-id"
Sheets_Convocatoria_ECO="google-sheet-id-for-ecolombia-convocatoria"
Sheets_Colsubsidio="google-sheet-id-for-colsubsidio"
Sheets_JAE="google-sheet-id-for-jae"
Sheets_Seguimiento_Suba="google-sheet-id-for-suba-seguimiento"
Sheets_ECO="google-sheet-id-for-ecolombia-seguimiento"
Data_suba_empleabilidad="google-sheet-id-for-suba-empleabilidad"
Sheets_Satisfaccion_Suba="google-sheet-id-for-suba-satisfaccion"
Data_looker_suba="google-sheet-id-for-suba-looker-data"
BQ_Caracterizacion="your-bigquery-dataset-id.your-bigquery-table-caracterizacion"
BQ_Empleabilidad="your-bigquery-dataset-id.your-bigquery-table-empleabilidad"
BQ_Satisfaccion="your-bigquery-dataset-id.your-bigquery-table-satisfaccion"
BQ_Seguimiento="your-bigquery-dataset-id.your-bigquery-table-seguimiento"
```

### 4.4 Autenticación de Google Cloud

Este proyecto utiliza una cuenta de servicio de Google Cloud para autenticarse con BigQuery y Google Sheets.

1.  **Crear una Cuenta de Servicio**: En su proyecto de Google Cloud, cree una cuenta de servicio.
2.  **Asignar Roles**: Asigne los roles necesarios a la cuenta de servicio:
    *   `Editor de datos de BigQuery` (o `Propietario de datos de BigQuery`) para escribir en BigQuery.
    *   `Lector de datos de BigQuery` para leer de BigQuery (para `Append_DATA_BQ.py` y `Limpieza_*.py`).
    *   `Editor` (o `Propietario`) para Google Sheets y Google Drive (para `gspread` y acceso a hojas).
3.  **Generar Clave JSON**: Genere una clave JSON para la cuenta de servicio.
4.  **Guardar Archivo**: Renombre el archivo JSON descargado a `credenciales.json` y colóquelo en la raíz del repositorio. **Este archivo debe ser tratado como sensible y no debe ser versionado.**

---

## 5. Lógica Principal y Pipeline

El proyecto se compone de varios scripts Python, cada uno con una función específica dentro del pipeline de datos.

### 5.1 Scripts de Ingestión de Datos (Upload)

Los scripts como `CONVOCATORIA_ECOLOMBIA_2026.py`, `Caracterizacion_*.py`, `Empleabilidad_*.py`, `Satisfaccion_*.py`, `UnificadoFormacion_*.py` y `Upload_*.py` son los encargados de la ingesta de datos.

**Lógica Común:**

1.  **Carga de Configuración**: Utilizan `python-dotenv` para cargar las variables de entorno (`PROJECT_ID`, `DATASET_ID`, `TABLE_ID`, `Sheets_ID`).
2.  **Autenticación**: Establecen conexión con Google Sheets (`gspread`) y Google BigQuery (`google-cloud-bigquery`) usando `credenciales.json`.
3.  **Extracción**: Leen datos de una hoja de cálculo específica de Google Sheets.
4.  **Pre-procesamiento de Headers**: Manejan casos donde los encabezados pueden estar en filas diferentes a la primera o contener celdas vacías.
5.  **Limpieza y Transformación (`pandas`)**:
    *   Eliminación de filas y columnas completamente vacías.
    *   Reemplazo de cadenas vacías o espacios en blanco por `None`/`NaN`.
    *   Eliminación de filas con valores nulos en columnas clave (e.g., `Número de Documento`).
    *   **Normalización de Nombres de Columnas**: Proceso robusto para estandarizar los nombres de las columnas:
        *   Convertir a minúsculas.
        *   Reemplazar espacios por guiones bajos.
        *   Eliminar caracteres especiales y saltos de línea.
        *   Normalizar caracteres Unicode (acentos, ñ) a ASCII.
        *   Manejar columnas duplicadas.
    *   **Conversión de Tipos de Datos**: Conversión explícita de columnas a tipos numéricos (enteros, flotantes), fechas, o porcentajes según corresponda.
    *   Adición de una columna `proyecto` para identificar la fuente de los datos.
6.  **Validación de Esquema**: Invocan la función `validar_y_comparar` del módulo `validacion_dataframes.py` para asegurar que el DataFrame resultante coincida con el esquema de la tabla de destino en BigQuery.
7.  **Carga a BigQuery**: Utilizan `client_bq.load_table_from_dataframe` con `write_disposition="WRITE_TRUNCATE"` para sobrescribir la tabla de destino en BigQuery, asegurando que los datos siempre estén actualizados. `autodetect=True` permite a BigQuery inferir los tipos de datos de las columnas si no se especifica un esquema explícito.

**Ejemplo de Normalización de Columnas (fragmento de código común):**

```python
DF.columns = (DF.columns
              .str.replace(" ","_")
              .str.normalize('NFKD')
              .str.encode('ascii', errors='ignore')
              .str.decode('utf-8')
              .str.lower()
              .str.replace(r"[\r\n]+", "", regex=True)
              .str.replace(r"[^a-z0-9_#]", "", regex=True)              
              )
```

### 5.2 Módulo de Validación de Esquemas (`validacion_dataframes.py`)

Este módulo es fundamental para la integridad del pipeline. Antes de cada carga a BigQuery, se invoca para comparar el esquema del DataFrame de origen con el esquema de la tabla de destino en BigQuery.

**Lógica:**

1.  Intenta obtener el esquema de la tabla de BigQuery. Si la tabla no existe, el script se detiene.
2.  Compara la cantidad de columnas entre el DataFrame y la tabla de BigQuery.
3.  Compara los nombres de las columnas (después de ordenarlos) para identificar discrepancias.
4.  Si hay diferencias en cantidad o nombres, reporta las columnas faltantes o sobrantes y detiene la ejecución del script de carga, evitando así cargas de datos corruptas o incompletas.

**Valor Agregado:**
Este módulo actúa como un **guardián de la calidad del esquema**, previniendo errores costosos en BigQuery que podrían surgir de cambios inesperados en las hojas de cálculo de origen. Permite **diagnosticar** problemas de estructura de datos en la fuente antes de que afecten el Data Warehouse, **acotando** el riesgo de inconsistencias y **estandarizando** la expectativa de los esquemas.

### 5.3 Script de Apéndice Histórico (`Append_DATA_BQ.py`)

Este script se encarga de mantener un registro histórico de ciertas tablas en BigQuery.

**Lógica:**

1.  Identifica tablas en BigQuery que contienen la palabra "unificado" (excluyendo "formacion" y "append").
2.  Para cada una de estas tablas, lee su contenido en un DataFrame de `pandas`.
3.  Agrega una columna `Fecha_Append` con el formato `YYYY-MM` (mes y año de la ejecución).
4.  Carga el DataFrame resultante en una tabla de BigQuery con el sufijo `_APPEND` (e.g., `SUBA_2026_UnificadoFormacion_APPEND`).
5.  Utiliza `write_disposition="WRITE_APPEND"` para añadir los nuevos registros a la tabla existente, creando un historial de los datos a lo largo del tiempo.

**Valor Agregado:**
Permite **medir** la evolución de los datos a lo largo del tiempo, facilitando análisis de tendencias y comparaciones históricas. Resuelve la necesidad de **periodización** de datos sin modificar las tablas transaccionales principales, y **estandariza** el proceso de captura de instantáneas históricas.

### 5.4 Scripts de Perfilado de Datos (`Limpieza_*.py`)

Los scripts `Limpieza_caracterizacion.py`, `Limpieza_empleabilidad.py`, `Limpieza_satisfaccion.py` y `Limpieza_seguimiento.py` son herramientas de diagnóstico de calidad de datos.

**Lógica:**

1.  Se conectan a BigQuery y consultan una tabla específica (definida por una variable de entorno `BQ_*`).
2.  Cargan los datos en un DataFrame de `pandas`.
3.  Iteran sobre las columnas del DataFrame (excluyendo algunas columnas identificadoras como 'Nombre', 'Documento', etc.).
4.  Para cada columna, imprimen los `value_counts()`, mostrando la distribución de valores únicos y la presencia de nulos.

**Valor Agregado:**
Estos scripts son cruciales para **diagnosticar** problemas de calidad de datos en las tablas de BigQuery. Permiten a los analistas **identificar** rápidamente valores inconsistentes, errores de entrada, patrones inesperados o la prevalencia de valores nulos en columnas críticas. Esto facilita la **optimización** de los procesos de recolección de datos y la **estandarización** de los criterios de calidad.

### 5.5 Orquestador de Ejecución (`trigger.py`)

Este script actúa como el punto de entrada principal para ejecutar el pipeline de ingesta de datos.

**Lógica:**

1.  Escanea el directorio actual para encontrar todos los archivos `.py`.
2.  Mantiene una lista de `archivos_excluidos` (como `trigger.py` mismo, scripts de limpieza, validación, etc.) para no ejecutarlos directamente.
3.  Itera sobre los scripts restantes (`scripts_ejecutables`) y los ejecuta uno por uno utilizando `subprocess.run()`.
4.  Reporta el éxito o fracaso de cada ejecución.
5.  Al final, resume si la actualización fue completa o si hubo fallos, listando los scripts problemáticos.

**Valor Agregado:**
El `trigger.py` **automatiza** la ejecución secuencial de los scripts de ingesta, **simplificando** la operación del pipeline. Permite **resolver** la complejidad de ejecutar múltiples scripts manualmente y **estandariza** el proceso de actualización de datos. Su sistema de reporte de fallos ayuda a **diagnosticar** rápidamente cualquier interrupción en el flujo de datos.

---

## 6. Ejemplos de Salida de Datos

### 6.1 DataFrame Limpio (Previo a BigQuery)

Este es un ejemplo de la estructura de un DataFrame después de la limpieza y normalización por uno de los scripts de ingesta, justo antes de ser cargado a BigQuery.

```
   numero_de_documento  tipo_de_documento     nombre_completo  fecha_nacimiento  edad  genero  ...  estado_actual  fecha_actualizacion  proyecto
0            101234567                CC  Persona Uno Ejemplo        1990-01-15    34  Masculino  ...       Activo           2024-07-20  Ecolombia 2.0
1            209876543                TI  Persona Dos Ejemplo        2005-03-22    19  Femenino  ...       Inactivo           2024-07-19  Ecolombia 2.0
2            304567890                CC  Persona Tres Ejemplo       1988-11-01    35  Masculino  ...       Activo           2024-07-21  Ecolombia 2.0
```

### 6.2 Tabla de Apéndice Histórico en BigQuery

Ejemplo de cómo se vería una tabla en BigQuery después de múltiples ejecuciones del script `Append_DATA_BQ.py`, mostrando la columna `Fecha_Append`.

```sql
-- Ejemplo de tabla: `your-gcp-project-id.your-bigquery-dataset-id.ECOPLUS_2026_CONVOCATORIA_APPEND`

SELECT
    numero_de_documento,
    nombre_completo,
    estado_actual,
    fecha_actualizacion,
    proyecto,
    fecha_append
FROM
    `your-gcp-project-id.your-bigquery-dataset-id.ECOPLUS_2026_CONVOCATORIA_APPEND`
LIMIT 5;
```

| numero_de_documento | nombre_completo     | estado_actual | fecha_actualizacion | proyecto      | fecha_append |
| :------------------ | :------------------ | :------------ | :------------------ | :------------ | :----------- |
| 101234567           | Persona Uno Ejemplo | Activo        | 2024-07-20          | Ecolombia 2.0 | 2024-07      |
| 209876543           | Persona Dos Ejemplo | Inactivo      | 2024-07-19          | Ecolombia 2.0 | 2024-07      |
| 101234567           | Persona Uno Ejemplo | Activo        | 2024-08-20          | Ecolombia 2.0 | 2024-08      |
| 209876543           | Persona Dos Ejemplo | Activo        | 2024-08-19          | Ecolombia 2.0 | 2024-08      |
| 304567890           | Persona Tres Ejemplo| Activo        | 2024-08-21          | Ecolombia 2.0 | 2024-08      |

---

## 7. Valor de Negocio y Capacidades Analíticas

Este pipeline de datos no es solo una solución técnica; es una herramienta estratégica que potencia la inteligencia de negocio y la gestión de proyectos.

### 7.1 Lo que se Muestra

El sistema consolida y presenta una visión unificada de los datos operativos de múltiples programas. Esto incluye:
*   **Datos de Caracterización**: Perfiles demográficos, socioeconómicos y educativos de los participantes.
*   **Datos de Convocatoria y Seguimiento**: Información sobre el proceso de inscripción, estado de los participantes en las fases del programa, y progreso en la formación.
*   **Datos de Empleabilidad**: Seguimiento de postulaciones, remisiones, colocaciones laborales y resultados de inserción.
*   **Datos de Satisfacción**: Feedback de los participantes sobre la calidad de los programas y servicios.
*   **Datos Históricos**: Instantáneas mensuales de la evolución de los indicadores clave.

### 7.2 Lo que Permite Medir

*   **Eficacia de los Programas**: Tasas de conversión en convocatorias, tasas de finalización de formación, tasas de empleabilidad.
*   **Impacto Social**: Número de beneficiarios, perfiles de población atendida, mejora en condiciones de empleabilidad.
*   **Rendimiento Operacional**: Tiempos de ciclo en procesos, eficiencia en la gestión de participantes.
*   **Satisfacción del Usuario**: Net Promoter Score (NPS), niveles de satisfacción con diferentes componentes del programa.
*   **Evolución Temporal**: Tendencias en todos los indicadores a lo largo del tiempo, gracias a los apéndices históricos.

### 7.3 Lo que Permite Diagnosticar

*   **Cuellos de Botella**: Identificar fases del programa con baja retención o conversión.
*   **Problemas de Calidad de Datos**: Detectar inconsistencias, valores atípicos o datos faltantes en las fuentes originales (Google Sheets) a través de los scripts de perfilado y validación.
*   **Ineficiencias en la Recolección de Datos**: Señalar áreas donde la entrada manual de datos es propensa a errores o ambigüedades.
*   **Desviaciones del Plan**: Comparar el progreso real con los objetivos establecidos para cada programa.
*   **Necesidades de Formación**: Identificar brechas en las habilidades de los participantes o en la oferta formativa.

### 7.4 Lo que Permite Resolver

*   **Silos de Información**: Unificar datos dispersos en múltiples hojas de cálculo en un único Data Warehouse.
*   **Inconsistencias de Datos**: Aplicar reglas de limpieza y normalización estandarizadas para asegurar la coherencia.
*   **Retrasos en la Generación de Informes**: Automatizar la ingesta de datos, reduciendo el tiempo de preparación para el análisis.
*   **Decisiones Basadas en Datos Obsoletos**: Proporcionar datos actualizados y validados de forma regular.
*   **Errores Humanos**: Minimizar la intervención manual en el proceso de ETL.

### 7.5 Lo que Permite Acotar

*   **Riesgos de Calidad de Datos**: La validación de esquemas y el perfilado de datos limitan la entrada de información errónea o mal estructurada.
*   **Ambigüedad en las Definiciones**: La normalización de columnas y la estandarización de tipos de datos acotan la interpretación de los campos.
*   **Costos Operacionales**: La automatización reduce la necesidad de recursos humanos dedicados a tareas repetitivas de ETL.
*   **Alcance de los Problemas**: Al diagnosticar rápidamente las fallas, se puede acotar el impacto de los errores en el sistema.

### 7.6 Lo que Permite Optimizar

*   **Procesos de Reporte y Análisis**: Al tener datos limpios y estructurados en BigQuery, la creación de dashboards y análisis ad-hoc es más rápida y fiable.
*   **Asignación de Recursos**: Identificar dónde los recursos (humanos, financieros) están generando el mayor impacto o dónde se necesitan más.
*   **Estrategias de Intervención**: Ajustar los programas de formación o empleabilidad basándose en el rendimiento y la satisfacción de los participantes.
*   **Experiencia del Participante**: Mejorar los puntos de contacto y servicios al entender mejor las necesidades y el feedback de los usuarios.
*   **Eficiencia del Pipeline**: El orquestador `trigger.py` optimiza la ejecución de los scripts, garantizando que el proceso sea robusto y eficiente.

### 7.7 Lo que Permite Estandarizar

*   **Modelos de Datos**: Crear un modelo de datos consistente y unificado en BigQuery para todos los proyectos.
*   **Procesos ETL**: Establecer un pipeline de ingesta, limpieza y carga uniforme para nuevas fuentes de datos.
*   **Métricas e Indicadores**: Definir métricas clave de manera consistente en todos los programas, permitiendo comparaciones significativas.
*   **Calidad de Datos**: Implementar un conjunto de reglas de limpieza y validación que se aplican de forma homogénea.
*   **Documentación y Gobernanza**: Al tener un proceso automatizado y bien definido, se facilita la documentación y la gobernanza de los datos.

### 7.8 Lo que Permite Repensar

*   **Estrategias de Recolección de Datos**: Al identificar problemas recurrentes en las fuentes, se puede repensar cómo se recopila la información desde el origen.
*   **Diseño de Programas**: Utilizar los insights generados para rediseñar o mejorar los programas de formación y empleabilidad, haciéndolos más efectivos y alineados con las necesidades del mercado.
*   **Interacción con los Participantes**: Repensar cómo se interactúa con los beneficiarios basándose en los datos de satisfacción y seguimiento.
*   **Infraestructura de Datos**: Evaluar la necesidad de herramientas adicionales o cambios en la arquitectura para soportar un crecimiento futuro.
*   **Cultura de Datos**: Fomentar una cultura donde las decisiones se basan en datos fiables y accesibles, transformando la organización en una entidad más orientada a datos.