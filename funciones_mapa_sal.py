# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:21:56 2022

@author: gramirez
"""

from modulos import *
from scipy.interpolate import griddata
import scipy as sp
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
import geojsoncontour
import scipy.ndimage
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def mapa_sal(ctd_por_mes_dict, variable, profundidad):
    
    coordenadas = (-12.25, -77.45)
    
    mapa = folium.Map(
          location = coordenadas,
          zoom_start = 6		
      )
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

    MousePosition(
       position="topright",
       separator=" | ",
       empty_string="NaN",
       lng_first=True,
       num_digits=20,
       prefix="Coordenadas:",
       lat_formatter=formatter,
       lng_formatter=formatter,
    ).add_to(mapa)
    
#=====================
    datos_dict = organizar_datos( ctd_por_mes_dict, variable, profundidad )
#=====================
    lats = []
    lons = []
    vals = []
    for mes, valores_mapa_zip in datos_dict.items():                
       for ids, lat, lon, valor in valores_mapa_zip:        
           popup = folium.Popup(max_width=450)             
           folium.Marker(location=[lat, lon], 
             popup = popup,
             icon = plugins.BeautifyIcon(iconSize=[10, 10], number = '{:.3f}'.format(valor))).add_to(mapa)
           lats.append( lat )
           lons.append( lon )
           vals.append( valor )
           
    minvar = min(vals)
    maxvar = max(vals)

    levels = 40
    cm     = branca.colormap.LinearColormap(['blue', 'yellow', 'red'],\
                                            vmin=minvar, vmax=maxvar).to_step(levels)        
    
    y = np.asarray(lats)
    x = np.asarray(lons)
    z = np.asanyarray(vals)
    
    with open('grid_mask.pkl', 'rb') as f:
       grid_mask = pickle.load(f) 
    
    with open('x_mesh.pkl', 'rb') as f:
       x_mesh = pickle.load(f)

    with open('y_mesh.pkl', 'rb') as f:
       y_mesh = pickle.load(f)   
    
    z_mesh = griddata((x, y), z, (x_mesh, y_mesh), method='cubic')
    
    sigma = [3, 3]
    
    z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='wrap')

#%%
    zv = np.reshape(z_mesh, (500*500,) )
    zmask = [ z if m else np.nan for z, m in zip( zv, grid_mask )  ]
    z_mesh = np.reshape(zmask, (500,500) )
    
#%%    
    
    mapa_color = plt.cm.get_cmap('RdYlBu')
    mapa_color_rev = mapa_color.reversed() 
    
    contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, cmap=mapa_color_rev, linestyles='None', vmin=minvar, vmax=maxvar)
    
    geojson = geojsoncontour.contourf_to_geojson(
    contourf=contourf,
    min_angle_deg=3.0,
    ndigits=3,
    stroke_width=1,
    fill_opacity=0.1)
    
    folium.GeoJson(
    geojson,
    style_function=lambda x: {
        'color':     x['properties']['stroke'],
        'weight':    x['properties']['stroke-width'],
        'fillColor': x['properties']['fill'],
        'opacity':   1,
    }).add_to(mapa)
    
    if variable=='salinidad':
       cm.caption = 'UPS'
    if variable=='temperatura':
       cm.caption = '°C'
    if variable=='v.sonido':
       cm.caption = 'm/s' 
       
    mapa.add_child(cm)
    plugins.Fullscreen(position='topright', force_separate_button=True).add_to(mapa)
    
    return mapa
#%%

def organizar_datos(ctd_por_mes_dict, variable, profundidad):
    resultado = {}
    
    for mes, lista_ctd in ctd_por_mes_dict.items():
        valores_mapa = pd.DataFrame()
        for ctd in lista_ctd:
           df = ctd.datos
           df = df[ df.variable == variable ]
           df = df[ df.profundidad == profundidad ]
           nr = len(df)
           ids = [ ctd.id for x in range(nr) ]
           lo = [ ctd.lon for x in range(nr) ]
           la  = [ ctd.lat for x in range(nr) ]
           ddff = pd.DataFrame( {'ids':ids,  'lat':la, 'lon':lo, 'val':df.valor} ).reset_index(drop=True)
           if (not ddff.empty):
              # print('*****************************')
              # print(ddff)
              valores_mapa = pd.concat([valores_mapa, ddff] )
        resultado[mes] = zip(valores_mapa.ids, valores_mapa.lat, valores_mapa.lon, valores_mapa.val)
    return resultado  



   




