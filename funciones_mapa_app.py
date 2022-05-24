# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:23:23 2022

@author: Gerardo
"""
from modulos import *

def cruceros_por_anio(lista_ctd, anio):

    ncolores = 12
    colores = sns.color_palette("hls", ncolores).as_hex()
    color_dict = { mes_esp[mes_unico[ii]] : colores[ii]    for ii in range(ncolores) }
    lista_ctd_mes = { 'Ene':[], 'Feb':[], 'Mar':[], 'Abr':[], 'May':[],\
                  'Jun':[], 'Jul':[], 'Ago':[], 'Set':[], 'Oct':[], 'Nov':[], 'Dic':[] } 
    
    cruceros = { anio:[] for anio in range(1994,2019) }
    
    for ctd_mes in lista_ctd:
        for ctd in ctd_mes:
            cruceros[ctd.fecha.year].append( ctd )
        
    for ctd in cruceros[anio]:
        lista_ctd_mes[ mes_esp[ctd.mes] ].append( ctd )
    lista_ctd_mes = dict( [ (k, v) for k, v in lista_ctd_mes.items() if len(v)>0 ] )    
    
    lgd_txt = '<span style="color: {col};">{txt}</span>'
        
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

    mapa.fit_bounds([[-20, -90],[-5, -70]]) 
    for mes, ctd_mes in lista_ctd_mes.items():
       grupo_mes = folium.FeatureGroup(\
                                    name = lgd_txt.format( txt = mes,\
                                                          col = color_dict[mes]))
       mapa.add_child(grupo_mes)
       [ ad_to_map( grupo_mes, ctd, color_dict) for ctd in ctd_mes ]
       grupo_mes.add_to(mapa)
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    with open('capa_mapa.json','w') as f:
        print(grupo_mes.to_json(), file=f)
    
    return mapa, lista_ctd_mes 


def numero_perfiles( diccionario_ctd ):
    nperfiles = 0
    for key in diccionario_ctd.keys():
        nperfiles += len(diccionario_ctd[key])
    return nperfiles    

