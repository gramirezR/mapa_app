# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:38:44 2022

@author: gramirez
"""

import pandas as pd
# import numpy as np
import re
import os
import io

#%%

archivos = [ f for f in os.listdir('.') 
            if re.match(r'datos_ctd_[A-za-z]{3}\.pkl', f) ]


meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic']

archivos_orden = [ f for mes in meses for f in archivos if mes in f   ]

print(archivos_orden)

ctd_df = pd.read_pickle( archivos[1] )
# print(ctd_df[['profundidad', 'variable', 'valor']].head())

mes_esp = {'January':'Enero', 'February':'Febrero', 'March':'Marzo', 'April':'Abril',\
           'May':'Mayo', 'June':'Junio', 'July':'Julio', 'August':'Agosto',\
               'September':'Setiembre', 'October':'Octubre', 'November':'Noviembre',\
                   'December':'Diciembre'}

# print( mes_esp[ctd_df.mes.iloc[0]] ) 

# 'Ene' in archivos[3]

#%%

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
        return self.fecha
    
    def datos(self):
        return self.datos
    
#%%
ctd_lista = []
for archivo in archivos_orden:   
   ctd_df = pd.read_pickle( archivo )
   ids = ctd_df.id.unique()
   temp = []
   for id in ids:              
       temp.append( CTD( ctd_df[ ctd_df.id==id ] ) )
   ctd_lista.append(temp)

#%%

# print( repr( ctd_lista[11][5] ) )

#%%
import pickle
with open('datos_ctd_obj.pkl', 'wb') as f:
    pickle.dump( ctd_lista, f )

# abril, agosto
# diciembre
# enero
# febrero
# junio, julio
# marzo, mayo
# noviembre
# octubre
# septiembre










