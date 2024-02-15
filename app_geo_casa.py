import pandas as pd
import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as stc
import folium
from streamlit_folium import st_folium

# Importo los ficheros
df_barrios = gpd.read_parquet("C:/Users/34610/Desktop/Master/1-Semestre/Proyecto_6/data/barrios.parquet")
df_pisos = gpd.read_parquet("C:/Users/34610/Desktop/Master/1-Semestre/Proyecto_6/data/pisos.parquet")



def main():
    # Título y literatura de la App
    stc.html('''
        <div style="background-color:MediumSeaGreen;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">HomApp</h1>
        <h4 style="color:white;text-align:center;">App para encontrar tu lugar</h4>
        </div>
        ''')

    #st.header('HomeApp')
    st.write('''Con esta app podrás filtrar mediante la barra lateral de la izquierda por barrios, 
        tipo de habitación y precio.''')
    st.info('Tienes una lista de los barrios justo de bajo del mapa :smile:')
    st.success('Al clicar en la ubicación puedes ver el tipo de vivienda y su precio')
    st.sidebar.header('Filtros')

    st.subheader('Mapa')

    # Filto por barrios
    barrios_disponibles = df_barrios['neighbourhood'].unique().tolist()
    barrio_seleccionado = st.sidebar.selectbox('Barrios', barrios_disponibles)

    # Filtro por habitación
    tipos_habitacion = df_pisos['room_type'].unique().tolist()
    tipo_habitacion_seleccionado = st.sidebar.selectbox('Tipo de habitación', tipos_habitacion)

    # Filtro por precio
    precios = df_pisos['price_sensation'].unique().tolist()
    precio = st.sidebar.selectbox('Precio', precios)

    # Uno los filtros para que se unan en un solo mapa
    df_filtrado = df_pisos[(df_pisos['room_type'] == tipo_habitacion_seleccionado) & 
    (df_pisos['price_sensation'] == precio) &
                           (df_pisos['coord'].apply(
                            lambda geom: geom.within(
                                df_barrios[df_barrios['neighbourhood'] == barrio_seleccionado]['geometry'].iloc[0])))]

    # Genero el mapa
    mapa = folium.Map(location=[40.4167, -3.70325], zoom_start=10, width=800, height=800)

    for index, row in df_filtrado.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['room_type'] + ' Precio = ' + str(row['price']) + '€'
        ).add_to(mapa)

    st_folium(mapa)

    # Creo visualización de posibles zonas
    st.subheader('Lista de los barrios disponibles en la app')

    lista_barrios = df_barrios.neighbourhood.unique()
    elem_por_columna = len(lista_barrios) // 3

    parte1 = lista_barrios[:elem_por_columna]
    parte2 = lista_barrios[elem_por_columna:2*elem_por_columna]
    parte3 = lista_barrios[2*elem_por_columna:]
    with st.expander(':mag:'):
        col1, col2, col3 = st.columns([2,2,2])
        with col1:
            st.write(parte1)
        with col2:
            st.write(parte2)
        with col3:
            st.write(parte3)

        #st.write([parte1, parte2, parte3])

if __name__ == '__main__':
    main()
