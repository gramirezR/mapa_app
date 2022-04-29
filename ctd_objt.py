# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 11:40:48 2022

@author: gramirez
"""

import io, folium, altair, json
from folium import plugins


mes_esp = {'January':'Ene', 'February':'Feb',
            'March':'Mar', 'April':'Abr', 'May':'May',
            'June':'Jun', 'July':'Jul', 'August':'Ago',
            'September':'Set', 'October':'Oct', 'November':'Nov', 'December':'Dic'}

class CTD:
    def __init__(self, df):
        self.datos = df[['profundidad', 'variable', 'valor']]
        self.id = df.id[0]
        self.mes = df.mes[0]
        self.fecha = df.fecha[0]
        self.lon = df.lon[0]
        self.lat = df.lat[0] 
    
    def __repr__(self):
         info = io.StringIO()
         self.datos.info(buf = info)
         titulo = 'Marina de Guerra del Perú\n'+\
             'Dirección de Hidrografía y Navegación\n'
         salida = titulo + \
             'Perfil hecho en: {}\nEn las coordenadas {}\nProfundidad máxima: {:.1f} metros \nCon variables: {} \n{}'.\
             format( self.fecha, (self.lon, self.lat), self.datos.profundidad.max() ,\
                    str(self.datos.variable.unique()), info.getvalue()  )
         return salida
    
    def id(self):
        return self.id
    
    def coordenadas(self):
        return (self.lon, self.lat)
    
    def fecha(self):
        type(self.fecha)
        return self.fecha
    
    def datos(self):
        return self.datos
    
def ad_to_map( mapa, ctd_obj, color_dict):
    df = ctd_obj.datos
    coords = ctd_obj.coordenadas()
    mes = mes_esp[ctd_obj.mes]
    anio_ctd = ctd_obj.fecha
    # print( coords[0], coords[1] )
    
    chart = altair.Chart(df
          ).mark_circle(
              size=7
          ).encode(
#           x = altair.X('valor', scale=altair.Scale(zero=False)),
            x = altair.X('valor', scale=altair.Scale(zero=False)),
            y = altair.Y('profundidad', scale=altair.Scale(reverse=True) )
          ).properties(
            width = 100,
            height = 300
          ).facet(
            column = 'variable' 
          ).resolve_scale(
            x='independent',
            y='shared')
    # json_chart =  chart.to_json( )         
    # chart_2 = json.loads(json_chart)
    popup = folium.Popup(max_width=450)   
    folium.features.VegaLite(chart, height=150, width=400).add_to(popup)  # pop-up label for the marker   
    folium.Marker(location=[coords[1], coords[0]], # coordinates for the marker (Earth Lab at CU Boulder)
        popup = popup,
        icon = plugins.BeautifyIcon(iconSize=[10, 10], number = int(anio_ctd.year),
        background_color = color_dict[mes],
        border_width=1,
        text_color='black',
        inner_icon_style='font-size:10px;margin-top:4px;')
    ).add_to(mapa)    