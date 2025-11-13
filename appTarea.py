import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Entrega de Proyectos de Análisis de Datos", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
st.title("Programación Avanzada")


df = pd.read_csv("Listado.csv")

df["RH"] = df["RH"].str.replace('0', 'O', regex=False)

df = df.drop('Unnamed: 10', axis=1)

df["Estatura"] = df["Estatura"].str.replace(',', '.')

df["Estatura"] = pd.to_numeric(df["Estatura"], errors='coerce')
df["Peso"] = pd.to_numeric(df["Peso"], errors='coerce')

df["Estatura_cm"] = df["Estatura"] * 100
df["IMC"] = df["Peso"] / (df["Estatura"]) ** 2

df["Clasificacion_IMC"] = pd.cut(
    df["IMC"],
    bins=[0, 18.5, 24.9, 29.9, np.inf],
    labels=["Bajo peso", "Normal", "Sobrepeso", "Obesidad"]
)

df['Color_Cabello'] = df['Color_Cabello'].str.capitalize()

df['Barrio_Residencia'] = df['Barrio_Residencia'].str.title()

df["Edad"] = df["Fecha_Nacimiento"].apply(
    lambda x: 2025 - int(x.split('/')[2]) if pd.notnull(x) else np.nan
)


st.sidebar.header("Parámetros")
with st.sidebar:
    RH = st.multiselect(
        "Tipo de Sangre (RH)",
        options=df["RH"].unique()
    )

    CC = st.multiselect(
        "Color de Cabello",
        options=df["Color_Cabello"].unique()
    )

    BR = st.multiselect(
        "Barrio de Residencia",
        options=df["Barrio_Residencia"].unique()
    )

    Integrantes = st.multiselect(
        "Integrantes",
        options=["ANDRÉS FELIPE YEPES TASCÓN", "JUAN DAVID PEREZ RESTREPO", "DAVID MAURICIO RESTREPO MEJIA"]
    )

    # Slider
    RE = st.slider(
        "Selecciona un rango de edad:",
        min_value=int(df["Edad"].min()),
        max_value=int(df["Edad"].max()),
        value=(int(df["Edad"].min()), int(df["Edad"].max()))
    )

    REs = st.slider(
        "Selecciona un rango de estatura (cm):",
        min_value=int(df["Estatura_cm"].min()),
        max_value=int(df["Estatura_cm"].max()),
        value=(int(df["Estatura_cm"].min()), int(df["Estatura_cm"].max()))
    )




# Filtrar el dataframe
df_filtrado = df.copy()

if RH:
    df_filtrado = df_filtrado[df_filtrado["RH"].isin(RH)]

if CC:
    df_filtrado = df_filtrado[df_filtrado["Color_Cabello"].isin(CC)]

if BR:
    df_filtrado = df_filtrado[df_filtrado["Barrio_Residencia"].isin(BR)]

Nombre_Apellido = df_filtrado["Nombre_Estudiante"] + " " + df_filtrado["Apellido_Estudiante"]

if Integrantes:
    df_filtrado = df_filtrado[Nombre_Apellido.isin(Integrantes)]

df_filtrado = df_filtrado[(df_filtrado["Edad"] >= RE[0]) & (df_filtrado["Edad"] <= RE[1])]

df_filtrado = df_filtrado[(df_filtrado["Estatura_cm"] >= REs[0]) & (df_filtrado["Estatura_cm"] <= REs[1])]


st.dataframe(df_filtrado)


st.header("Dashboard Estudiantil - Grupo 001")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    total_students = df_filtrado.shape[0]
    st.metric("Total Estudiantes", f"{total_students}")
with c2:
    promedio_edad = df_filtrado["Edad"].mean()
    st.metric("Edad Promedio", f"{promedio_edad:.1f} años")
with c3:
    promedio_estatura = df_filtrado["Estatura_cm"].mean()
    st.metric("Estatura Promedio", f"{promedio_estatura:.1f} cm")
with c4:
    promedio_peso = df_filtrado["Peso"].mean()
    st.metric("Peso Promedio", f"{promedio_peso:.1f} kg")
with c5:
    IMC_promedio = df_filtrado["IMC"].mean()
    st.metric("IMC Promedio", f"{IMC_promedio:.1f}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

sns.countplot(data=df_filtrado, x='Edad', ax=ax1)
ax1.tick_params(axis='x', rotation=45)
ax1.set_xlabel("Edad")
ax1.set_ylabel("Número de Estudiantes")

df_filtrado['RH'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
ax2.set_xlabel("Tipo de Sangre (RH)")
ax2.set_ylabel("")

plt.tight_layout()
st.pyplot(fig)


fig, (ax, ax1) = plt.subplots(1, 2, figsize=(12, 5))

sns.scatterplot(data=df_filtrado, x='Estatura_cm', y='Peso', ax=ax)
ax.set_xlabel("Estatura (cm)")
ax.set_ylabel("Peso (kg)")

sns.countplot(data=df_filtrado, x='Color_Cabello', ax=ax1)
ax1.tick_params(axis='x', rotation=45)
ax1.set_xlabel("Color de Cabello")
ax1.set_ylabel("Número de Estudiantes")

st.pyplot(fig)


fig, (ax, ax1) = plt.subplots(1, 2, figsize=(12, 5))

sns.lineplot(data=df_filtrado, x='Estatura_cm', y='Talla_Zapato', ax=ax)
ax.set_xlabel("Estatura (cm)")
ax.set_ylabel("Talla de Zapato")

top_10_barrios = df_filtrado['Barrio_Residencia'].value_counts().head(10)
df_top10 = df_filtrado[df_filtrado['Barrio_Residencia'].isin(top_10_barrios.index)]

sns.countplot(data=df_top10, x='Barrio_Residencia', order=top_10_barrios.index, ax=ax1)
ax1.tick_params(axis='x', rotation=45)
ax1.set_xlabel("Barrio de Residencia")
ax1.set_ylabel("Número de Estudiantes")

st.pyplot(fig)

st.subheader("Top 5 Estudiantes")

col1, col2 = st.columns(2)

top5_estatura = df_filtrado.nlargest(5, 'Estatura_cm')[['Nombre_Estudiante', 'Apellido_Estudiante', 'Estatura_cm']]
top5_peso = df_filtrado.nlargest(5, 'Peso')[['Nombre_Estudiante', 'Apellido_Estudiante', 'Peso']]

with col1:
    st.download_button(
        label="📥 Descargar Top 5 Estatura",
        data=top5_estatura.to_csv(index=False).encode('utf-8'),
        file_name='top5_estatura.csv',
        mime='text/csv'
    )

with col2:
    st.download_button(
        label="📥 Descargar Top 5 Peso",
        data=top5_peso.to_csv(index=False).encode('utf-8'),
        file_name='top5_peso.csv',
        mime='text/csv'
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Estatura")
    st.write(df_filtrado["Estatura_cm"].describe())

with col2:
    st.subheader("Peso")
    st.write(df_filtrado["Peso"].describe())

with col3:
    st.subheader("IMC")
    st.write(df_filtrado["IMC"].describe())