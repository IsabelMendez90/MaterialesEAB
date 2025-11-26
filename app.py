import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.set_page_config(page_title="Ficha Técnica de Materiales", layout="wide")
st.title("📄 Ficha Técnica de Materiales de Construcción con apoyo de Mentor AI para AR2007B.545")
st.markdown("Creadora: Dra. J. Isabel Méndez Garduño")

# Cargar base de datos
df = pd.read_excel("materiales_energyplus.xlsx")

# Inicializar estado
if "respuestas_ai" not in st.session_state:
    st.session_state.respuestas_ai = {}

# === SECCIÓN 1: Consulta desde Excel ===
st.subheader("📂 Consulta materiales precargados")
materiales = df["Nombre"].tolist()
seleccionados = st.multiselect("Selecciona uno o más materiales:", materiales)

if seleccionados:
    for nombre in seleccionados:
        st.header(f"🧱 {nombre}")
        fila = df[df["Nombre"] == nombre].iloc[0]

        st.subheader("📐 Propiedades Físicas")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- **Nombre en Inglés:** {fila['Name(EN)']}")
            st.markdown(f"- **Densidad:** {fila['Densidad (kg/m3)']} kg/m³")
            st.markdown(f"- **Conductividad térmica:** {fila['Conductividad (W/m-K)']} W/m·K")
        with col2:
            st.markdown(f"- **Calor específico:** {fila['Calor Específico (J/kg-K)']} J/kg·K")
            st.markdown(f"- **Rugosidad superficial:** {fila['Rugosidad superficial']}")
            st.markdown(f"- **Tipo:** {fila['Tipo']}")

        st.subheader("🧪 Propiedades Químicas, Ciclo de Vida y Recomendaciones (Mentor AI)")
        if nombre in st.session_state.respuestas_ai:
            st.info(st.session_state.respuestas_ai[nombre])

        if st.button(f"🔎 Consultar Mentor AI sobre '{nombre}'"):
            try:
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=st.secrets["OPENROUTER_API_KEY"]
                )

                prompt = f"""
Genera una ficha técnica completa y detallada del siguiente material de construcción: {nombre}.

1. 🧱 Propiedades Físicas:
   - Nombre técnico en inglés
   - Densidad en kg/m³
   - Conductividad térmica en W/m·K
   - Calor específico en J/kg·K
   - Rugosidad superficial (Liso / Medio / Rugoso)
   - Tipo de material (estructura, acabado, aislante, etc.)

2. 🧪 Propiedades químicas y comportamiento:
   - Composición química general
   - Si es inerte o emite compuestos
   - Resistencia al fuego y a la corrosión

3. 🌱 Sostenibilidad y ciclo de vida:
   - Origen (natural, sintético, reciclado)
   - Impacto ambiental en producción y transporte
   - Posibilidad de reutilización o reciclaje

4. 🏗️ Recomendaciones arquitectónicas:
   - Usos recomendados (muros, techos, pisos, etc.)
   - Cuidados y mantenimiento
   - Compatibilidad con climas cálidos/húmedos

Proporciona valores numéricos realistas cuando sea posible. Usa formato claro y estructurado, sin hacer preguntas al usuario.
"""

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "Eres un arquitecto experto en materiales, sostenibilidad y diseño accesible en México. "
                            "Hablas en un lenguaje técnico y directo para estudiantes y profesionales de arquitectura."
                        )
                    },
                    {"role": "user", "content": prompt}
                ]

                completion = client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": "https://tudespacho-academico.com",
                        "X-Title": "Ficha Tecnica AI"
                    },
                    extra_body={},
                    model="deepseek/deepseek-chat-v3-0324:free",
                    messages=messages
                )

                respuesta = completion.choices[0].message.content
                st.session_state.respuestas_ai[nombre] = respuesta
                st.success("Respuesta del mentor AI almacenada.")
                st.markdown(respuesta)

            except Exception as e:
                st.warning(f"No se pudo conectar con el Mentor AI. Error: {e}")

# === SECCIÓN 2: Consulta libre ===
st.markdown("---")
st.subheader("🔍 ¿Quieres consultar otro material que no esté en la lista?")
material_libre = st.text_input("Escribe el nombre del material a consultar:")

if material_libre:
    if material_libre in st.session_state.respuestas_ai:
        st.info(st.session_state.respuestas_ai[material_libre])

    if st.button("🔎 Consultar ficha técnica extendida del material ingresado"):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=st.secrets["OPENROUTER_API_KEY"]
            )

            prompt = f"""
Genera una ficha técnica completa y detallada del siguiente material de construcción: {material_libre}.

1. 🧱 Propiedades Físicas:
   - Nombre técnico en inglés
   - Densidad en kg/m³
   - Conductividad térmica en W/m·K
   - Calor específico en J/kg·K
   - Rugosidad superficial (Liso / Medio / Rugoso)
   - Tipo de material (estructura, acabado, aislante, etc.)

2. 🧪 Propiedades químicas y comportamiento:
   - Composición química general
   - Si es inerte o emite compuestos
   - Resistencia al fuego y a la corrosión

3. 🌱 Sostenibilidad y ciclo de vida:
   - Origen (natural, sintético, reciclado)
   - Impacto ambiental en producción y transporte
   - Posibilidad de reutilización o reciclaje

4. 🏗️ Recomendaciones arquitectónicas:
   - Usos recomendados (muros, techos, pisos, etc.)
   - Cuidados y mantenimiento
   - Compatibilidad con climas cálidos/húmedos

Proporciona valores numéricos realistas cuando sea posible. Usa formato claro y estructurado, sin hacer preguntas al usuario.
"""

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Eres un arquitecto experto en materiales, sostenibilidad y diseño accesible en México. "
                        "Hablas en un lenguaje técnico y directo para estudiantes y profesionales de arquitectura."
                    )
                },
                {"role": "user", "content": prompt}
            ]

            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://tudespacho-academico.com",
                    "X-Title": "Ficha Tecnica AI"
                },
                extra_body={},
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=messages
            )

            respuesta = completion.choices[0].message.content
            st.session_state.respuestas_ai[material_libre] = respuesta
            st.success("Respuesta del mentor AI almacenada.")
            st.markdown(respuesta)

        except Exception as e:
            st.warning(f"No se pudo conectar con el Mentor AI. Error: {e}")
