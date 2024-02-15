import pandas as pd
import folium
import streamlit as st
import geopandas as gpd

from streamlit_folium import st_folium

df_barrios = gpd.read_file("C:/Users/34610/Desktop/Master/1-Semestre/9_Visualizacion_Avanzada_de_Datos/9_04_Geopandas/PC6/data/neighbourhoods.geojson")
df_pisos = pd.read_csv("C:/Users/34610/Desktop/Master/1-Semestre/9_Visualizacion_Avanzada_de_Datos/9_04_Geopandas/PC6/data/pisos.csv")

df_pisos['coord'] = gpd.points_from_xy(
    x=df_pisos.longitude, y=df_pisos.latitude
)
df_pisos = gpd.GeoDataFrame(df_pisos, geometry="coord")

sol_geom = df_barrios.loc[lambda df:df.neighbourhood == 'Sol'].iloc[0].geometry

df_pisos_sol = (
    df_pisos
    .assign(
        is_in_sol=lambda df: df.geometry.map(lambda g: sol_geom.contains(g))
    )
    .loc[lambda df:df.is_in_sol]
)

categorias = {
    '1_Muy barato':(0, 50),
    '2_Barato': (50, 100),
    '3_Precio medio': (100, 200),
    '4_Caro': (200, 1000),
    '5_Muy caro': (1000, 10000)
}

def texto_categoria(precio):
    for categoria, (min_price, max_price) in categorias.items():
        if min_price <= precio < max_price:
            return categoria
        

df_pisos_sol['price_sensation'] = df_pisos_sol['price'].apply(texto_categoria)

puerta_sol = [40.41711891959671, -3.703583017644129]
mapa = folium.Map(location=puerta_sol, zoom_start=10, width=800, height=800)

for categoria, data in df_pisos_sol.groupby('price_sensation'):
    layer = folium.FeatureGroup(name=categoria)
    for _, row in data.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['price_sensation']).add_to(layer)
    layer.add_to(mapa)
    
folium.LayerControl().add_to(mapa)

st_folium(mapa)



