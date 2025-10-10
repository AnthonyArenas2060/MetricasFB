import pandas as pd
import streamlit as st
import facebook
import requests
import matplotlib.pyplot as plt
import numpy as np




st.markdown("""
    <style>
        /* Cambiar color de fondo */
        .stApp {
            background-color: #f4f4f9;
        }

        /* Estilo para títulos */
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Poppins', sans-serif;
        }

        /* Tarjetas o contenedores personalizados */
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Metricas - Facebook Pages")

user_long_token = st.text_input("Introduce tu token de acceso (short-lived):", type="password")


if user_long_token:
    try:
        graph = facebook.GraphAPI(access_token=user_long_token, version="3.1")

        # 3️⃣ Inputs de fecha
        date_ini = st.date_input("Selecciona la fecha inicial")
        date_fin = st.date_input("Selecciona la fecha final")

        # 4️⃣ Obtener información de las páginas asociadas
        page_data = graph.get_object('/me/accounts')
        info = pd.DataFrame(page_data['data'])

        st.subheader("📋 Páginas asociadas a tu cuenta")
        st.dataframe(info['name'])

        # 5️⃣ Permitir seleccionar un número (por ejemplo, el índice de una fila)
        if not info.empty:
            indice = st.number_input(
                "Selecciona el número de fila que deseas usar:",
                min_value=0,
                max_value=len(info) - 1,
                step=1
            )
            if indice:
                st.write("Seleccionaste la página:")
                st.write(info['name'][indice])
                permanent_page_token = page_data['data'][indice]['access_token']
                page_id = page_data['data'][indice]['id']

                graph = facebook.GraphAPI(access_token=permanent_page_token, version=3.1)
                graph.get_object(id=page_id, fields='name')

                fans = graph.get_connections(id = page_id, connection_name = 'insights', metric = 'page_fans', since = date_ini, until = date_fin)
                dataframe_facebook = pd.DataFrame(fans['data'][0]['values'])
                dataframe_facebook.columns = ['Fans', 'Fecha']
                dataframe_facebook['Fecha'] = pd.to_datetime(dataframe_facebook['Fecha'])
                #dataframe_facebook['Fecha'] = dataframe_facebook['Fecha'].dt.strftime('%Y-%m-%d')
                df_fans = dataframe_facebook.set_index('Fecha')
                df_fans['Nuevos Fans Netos'] = df_fans['Fans'].diff(periods=1)
                df_fans['Nuevos Fans Netos'] = df_fans['Nuevos Fans Netos'].fillna(0)
                
                st.subheader("Fans asociados a tu cuenta")
                st.dataframe(dataframe_facebook)
                st.line_chart(
                                df_fans['Nuevos Fans Netos'],
                                y_label='Nuevos Fans Netos',
                                use_container_width=True
                            )
                

                posts = graph.get_connections(id=page_id, connection_name="feed", since=date_ini, until=date_fin)
                posteos = pd.DataFrame(posts['data'])
                posteos = posteos.iloc[:, :3]
                if not posteos.empty:
                    posteos.columns = ['Fecha', 'Mensaje', 'id']  # , 'stories']
                    posteos['Fecha'] = pd.to_datetime(posteos['Fecha'])
                    posteos['Fecha'] = posteos['Fecha'].dt.strftime('%Y-%m-%d')

                    st.subheader("📋 Post asociadas a tu cuenta")
                    st.dataframe(posteos)
                else:
                    st.write("No se encontraron publicaciones en el rango de fechas seleccionado.")


    except Exception as e:
        st.error(f"Ocurrió un error: {e}")



