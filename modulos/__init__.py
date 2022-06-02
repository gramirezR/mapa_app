# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:35:14 2022

@author: Gerardo
"""

import numpy as np
from flask import Flask, render_template, request, url_for, flash, redirect, session
import folium
import branca
from folium import plugins
from folium.plugins import MousePosition, HeatMap
import pandas as pd
import os, pickle
import seaborn as sns
import io, altair, json
from ctd_objt import * # CTD se usa al cargar los datos en df_ctd
from funciones_mapa_app import cruceros_por_anio, numero_perfiles
from funciones_mapa_sal import *
import jinja2
from jinja2 import Template

