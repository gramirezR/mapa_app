from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/mapa')
def mapa():
   coordenadas = (-12.25, -77.45)
   folium_map = folium.Map(
        location = coordenadas,
        zoom_start = 6		
    )
   folium.Marker(
         coordenadas,
         popup = '<i>Hola!</i>',
         icon = folium.Icon(color='blue', icon='cloud')
         ).add_to(folium_map)
         
   folium_map.save('templates/mapa.html')
   return render_template('mapa.html')
        
if __name__=='__main__':
   app.run(debug=True)   