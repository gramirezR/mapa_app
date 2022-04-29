from flask import Flask, render_template
import folium
import pandas as pd
import os
# from selenium import webdriver
from ctd_objt import CTD, ad_to_map # CTD se usa al cargar los datos en df_ctd
from funciones_mapa_app import cruceros_por_anio

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/mapa')
def mapa():
   df_ctd = pd.read_pickle( 'datos_ctd_obj.pkl' )
   # coordenadas = (-12.25, -77.45)
   # folium_map = folium.Map(
   #      location = coordenadas,
   #      zoom_start = 6		
   #  )
   # folium.Marker(
   #       coordenadas,
   #       popup = '<i>Hola!</i>',
   #       icon = folium.Icon(color='blue', icon='cloud')
   #       ).add_to(folium_map)
         
   # folium_map.save('templates/mapa.html')
   
   mapa_por_anio = cruceros_por_anio(df_ctd, 2006)

   nombre_mapa = 'mapa.html'
   mapa_templates = '{}/{}'.format( os.getcwd(), 'templates/'+nombre_mapa)
   mapa_por_anio.save(mapa_templates)

   # driver = webdriver.Firefox()
   # driver.get(mapUrl)
   return render_template(nombre_mapa)
        
if __name__=='__main__':
   app.run(debug=True)   