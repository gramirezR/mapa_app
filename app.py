from modulos import *

app = Flask(__name__)

app.secret_key = '31Ra09052oceano'

@app.route('/', methods=['GET', 'POST'])
def index():
    
   df_ctd = pd.read_pickle( 'datos_ctd_obj.pkl' )
   nombre_mapa = 'mapa.html'
   mapa_templates = '{}/{}'.format( os.getcwd(), 'templates/'+nombre_mapa)
   session['variable'] = 'Ahora estamos'
   if request.method == 'POST':
      anio = int( request.form['anio'] )
      mapa_por_anio, lista_ctd = cruceros_por_anio(df_ctd, anio)
      nperfiles = numero_perfiles( lista_ctd )
      mapa_por_anio.save(mapa_templates)
      return render_template('index.html', anio=anio, tamanio = nperfiles)
   else:
      anio = 1998
      mapa_por_anio, lista_ctd = cruceros_por_anio(df_ctd, anio)
      nperfiles = numero_perfiles( lista_ctd )
      mapa_por_anio.save(mapa_templates)  
      return render_template('index.html', anio=anio, tamanio = nperfiles)
  
@app.route('/mapa')
def mapa():
   return render_template('mapa.html')

@app.route('/tabla')
def tabla():
    valor = session.get('variable')
    return render_template('tabla.html', valor=valor)
        
if __name__=='__main__':
   app.run(debug=True)   