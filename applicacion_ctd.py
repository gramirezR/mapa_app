# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:02:20 2022

@author: gramirez
"""

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
# import json
import folium
# from folium import plugins
from selenium import webdriver
import altair
import seaborn as sns
from ctd_objt import CTD, ad_to_map # CTD se usa al cargar los datos en df_ctd
altair.data_transformers.disable_max_rows()
# altair.data_transformers.enable('json')
altair.renderers.set_embed_options(actions=False)
#%%

df_ctd = pd.read_pickle( 'datos_ctd_obj.pkl' )


#%%

# print( df_ctd[0][0] )

#%%

punto0 = [-12.587007 , -82.490214]

mes_unico = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']

mes_esp = {'January':'Ene', 'February':'Feb',
            'March':'Mar', 'April':'Abr', 'May':'May',
            'June':'Jun', 'July':'Jul', 'August':'Ago',
            'September':'Set', 'October':'Oct', 'November':'Nov', 'December':'Dic'}

ncolores = 12
colores = sns.color_palette("hls", ncolores).as_hex()
color_dict = { mes_esp[mes_unico[ii]] : colores[ii]    for ii in range(ncolores) }


datos_ctd = df_ctd[0][0]
#%%


cruceros = { anio:[] for anio in range(1994,2019) }

for ctd_mes in df_ctd:
    for ctd in ctd_mes:
        cruceros[ctd.fecha.year].append( ctd )

#%%


nombre_mapa = 'prueba.html'
mapUrl = 'file://{}/{}'.format( os.getcwd(), nombre_mapa)


lgd_txt = '<span style="color: {col};">{txt}</span>'


#%%

lista_ctd = cruceros[2018]

lista_ctd_mes = { 'Ene':[], 'Feb':[], 'Mar':[], 'Abr':[], 'May':[],\
                 'Jun':[], 'Jul':[], 'Ago':[], 'Set':[], 'Oct':[], 'Nov':[], 'Dic':[] }

m_2 = folium.Map(location=punto0, zoom_start = 6)
m_2.fit_bounds([[-20, -90],[-5, -70]]) 
for ctd in lista_ctd:
    lista_ctd_mes[ mes_esp[ctd.mes] ].append( ctd )   
    
lista_ctd_mes = dict( [ (k, v) for k, v in lista_ctd_mes.items() if len(v)>0 ] )
    
# print(lista_ctd_mes.values())

for mes, ctd_mes in lista_ctd_mes.items():
    grupo_mes = folium.FeatureGroup(\
                                    name = lgd_txt.format( txt = mes,\
                                                          col = color_dict[mes]))
    m_2.add_child(grupo_mes)
    [ ad_to_map( grupo_mes, ctd, color_dict) for ctd in ctd_mes ]
    grupo_mes.add_to(m_2)
folium.LayerControl(collapsed=False).add_to(m_2)
m_2.save(nombre_mapa)

driver = webdriver.Firefox()
driver.get(mapUrl)



