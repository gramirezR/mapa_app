from modulos import *

app = Flask(__name__)

##====================================================##
@app.route('/', methods=['GET', 'POST'])
def index():    
   df_ctd = pd.read_pickle( 'datos_ctd_obj.pkl' )
   nombre_mapa = 'mapa.html'
   mapa_templates = '{}/{}'.format( os.getcwd(), 'templates/'+nombre_mapa)
      
   if request.method == 'POST':
      anio = int( request.form['anio'] )
   else:
      anio = 1998
 
   mapa_por_anio, lista_ctd = cruceros_por_anio(df_ctd, anio)
   nperfiles = numero_perfiles( lista_ctd )
   mapa_por_anio.save(mapa_templates)
   with open('ctd_dict.pkl', 'wb') as f:
      pickle.dump(lista_ctd, f, protocol=pickle.HIGHEST_PROTOCOL)
   
   with open('anio.pkl', 'wb') as f:
      pickle.dump(anio, f, protocol=pickle.HIGHEST_PROTOCOL) 
      
   return render_template('index.html', anio=anio, tamanio = nperfiles)
##====================================================##    
@app.route('/mapa')
def mapa():
   return render_template('mapa.html')

@app.route('/tabla')
def tabla():
    with open('ctd_dict.pkl', 'rb') as f:
       lista_ctd = pickle.load(f)         
    return render_template('tabla.html', lista_ctd=lista_ctd)
##====================================================##
@app.route('/salinidad', methods=['GET', 'POST'])
def salinidad():
    with open('anio.pkl', 'rb') as f:
        anio = pickle.load(f)
        
    with open('ctd_dict.pkl', 'rb') as f:
       ctd_por_mes_dict = pickle.load(f)
    
    nombre_mapa = '{}/{}'.format( os.getcwd(), 'templates/mapa_salinidad.html')
    
    if request.method == 'POST':
       profundidad = int( request.form['profundidad'] )
    else:
       profundidad = 5
    
    mapa = mapa_sal(ctd_por_mes_dict, 'salinidad', profundidad)
    
    mapa.save(nombre_mapa)
     
    return render_template('pagina_salinidad.html', profundidad=profundidad, anio=anio)

@app.route('/mapa_salinidad')
def mapa_salinidad():
   return render_template('mapa_salinidad.html')    
##====================================================##
@app.route('/temperatura', methods=['GET', 'POST'])
def temperatura():
 
    with open('anio.pkl', 'rb') as f:
        anio = pickle.load(f)
        
    with open('ctd_dict.pkl', 'rb') as f:
       ctd_por_mes_dict = pickle.load(f)
    
    nombre_mapa = '{}/{}'.format( os.getcwd(), 'templates/mapa_temperatura.html')

    if request.method == 'POST':
       profundidad = int( request.form['profundidad'] )
    else:
       profundidad = 5
    
    mapa = mapa_sal(ctd_por_mes_dict, 'temperatura', profundidad)
    
    mapa.save(nombre_mapa)
     
    return render_template('pagina_temperatura.html', profundidad=profundidad, anio=anio)

@app.route('/mapa_temperatura')
def mapa_temperatura():
   return render_template('mapa_temperatura.html')  
##====================================================##
@app.route('/vsonido', methods=['GET', 'POST'])
def vsonido():
    
    with open('anio.pkl', 'rb') as f:
        anio = pickle.load(f)
        
    with open('ctd_dict.pkl', 'rb') as f:
       ctd_por_mes_dict = pickle.load(f)
    
    nombre_mapa = '{}/{}'.format( os.getcwd(), 'templates/mapa_vsonido.html')

    if request.method == 'POST':
       profundidad = int( request.form['profundidad'] )
    else:
       profundidad = 5
    
    mapa = mapa_sal(ctd_por_mes_dict, 'v.sonido', profundidad)
    
    mapa.save(nombre_mapa)
     
    return render_template('pagina_vsonido.html', profundidad=profundidad, anio=anio)

@app.route('/mapa_vsonido')
def mapa_vsonido():
   return render_template('mapa_vsonido.html')
##====================================================##
if __name__=='__main__':
   app.run(debug=True)

