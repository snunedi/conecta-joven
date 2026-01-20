from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
# Paso 1: Importamos las herramientas de seguridad
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'conecta_joven_2026_titulacion'

# Configuración Base de Datos Aiven
db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_pFwiEHMe7XalGTeSN7l',
    'host': 'db-conecta-joven-snunedi-afb6.j.aivencloud.com',
    'port': 18771,
    'database': 'defaultdb',
    'ssl_ca': 'ca.pem'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- NAVEGACIÓN PÚBLICA --- (Se mantiene igual)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bienestar')
def bienestar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM p_001_articulo_bienestar ORDER BY id_articulo DESC")
    articulos = cursor.fetchall()
    conn.close()
    return render_template('bienestar.html', articulos=articulos)

@app.route('/deportes', methods=['GET', 'POST'])
def deportes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM p_001_comuna ORDER BY nombre_comuna")
    comunas = cursor.fetchall()
    comuna_id = request.form.get('comuna')
    if comuna_id and comuna_id != "Todas":
        cursor.execute("SELECT a.*, c.nombre_comuna FROM p_001_actividad_deportiva a JOIN p_001_comuna c ON a.id_comuna = c.id_comuna WHERE a.id_comuna = %s", (comuna_id,))
    else:
        cursor.execute("SELECT a.*, c.nombre_comuna FROM p_001_actividad_deportiva a JOIN p_001_comuna c ON a.id_comuna = c.id_comuna")
    actividades = cursor.fetchall()
    conn.close()
    return render_template('deportes.html', actividades=actividades, comunas=comunas)

@app.route('/academia')
def academia():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT c.*, i.nombre_inst FROM p_001_carrera c JOIN p_001_institucion i ON c.id_institucion = i.id_institucion")
    carreras = cursor.fetchall()
    conn.close()
    return render_template('academia.html', carreras=carreras)

@app.route('/sos')
def sos():
    return render_template('emergencia.html')

# --- REGISTRO (NUEVO/NECESARIO) ---
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        # Generamos el hash de la contraseña para no guardarla en texto plano
        pass_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # id_rol 2 es para Jóvenes por defecto
            cursor.execute("INSERT INTO p_001_usuario (nombre_completo, email, password_hash, id_rol) VALUES (%s, %s, %s, %s)", 
                           (nombre, email, pass_hash, 2))
            conn.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error: El correo ya está registrado.', 'danger')
        finally:
            conn.close()
    return render_template('registro.html')

# --- PERFIL Y FAVORITOS --- (Se mantiene igual)
@app.route('/perfil')
def perfil():
    if 'user_id' not in session: return redirect(url_for('login'))
    if session.get('user_rol') == 1: return redirect(url_for('admin_panel'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.id_favorito, d.nombre_taller, d.precio, c.nombre_comuna 
        FROM p_001_favorito f 
        JOIN p_001_actividad_deportiva d ON f.id_recurso = d.id_actividad 
        JOIN p_001_comuna c ON d.id_comuna = c.id_comuna
        WHERE f.id_usuario = %s AND f.tipo_recurso = 'deporte'""", (session['user_id'],))
    fav_deportes = cursor.fetchall()
    cursor.execute("""
        SELECT f.id_favorito, car.nom_carrera, inst.nombre_inst, car.tiene_gratuidad
        FROM p_001_favorito f 
        JOIN p_001_carrera car ON f.id_recurso = car.id_carrera
        JOIN p_001_institucion inst ON car.id_institucion = inst.id_institucion
        WHERE f.id_usuario = %s AND f.tipo_recurso = 'academia'""", (session['user_id'],))
    fav_academia = cursor.fetchall()
    cursor.execute("""
        SELECT f.id_favorito, b.titulo 
        FROM p_001_favorito f 
        JOIN p_001_articulo_bienestar b ON f.id_recurso = b.id_articulo
        WHERE f.id_usuario = %s AND f.tipo_recurso = 'bienestar'""", (session['user_id'],))
    fav_bienestar = cursor.fetchall()
    conn.close()
    return render_template('perfil.html', fav_deportes=fav_deportes, fav_academia=fav_academia, fav_bienestar=fav_bienestar)

# (Rutas de agregar/eliminar favorito se mantienen iguales)
@app.route('/agregar_favorito', methods=['POST'])
def agregar_favorito():
    if 'user_id' not in session: return redirect(url_for('login'))
    id_rec = request.form.get('id_recurso')
    tipo = request.form.get('tipo_recurso')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO p_001_favorito (id_usuario, id_recurso, tipo_recurso) VALUES (%s, %s, %s)", 
                        (session['user_id'], id_rec, tipo))
        conn.commit()
        flash('Añadido a favoritos', 'success')
    except:
        flash('Ya está en tus favoritos', 'info')
    conn.close()
    return redirect(request.referrer)

@app.route('/eliminar_favorito/<int:id>')
def eliminar_favorito(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM p_001_favorito WHERE id_favorito = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('perfil'))

# --- PANEL ADMINISTRATIVO Y CRUD --- (Se mantiene igual)

@app.route('/admin')
def admin_panel():
    if session.get('user_rol') != 1: return redirect(url_for('login'))
    return render_template('admin_panel.html')

@app.route('/admin/bienestar', methods=['GET', 'POST'])
def admin_bienestar():
    if session.get('user_rol') != 1: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("INSERT INTO p_001_articulo_bienestar (titulo, contenido, id_autor) VALUES (%s, %s, %s)", 
                        (request.form['titulo'], request.form['contenido'], session['user_id']))
        conn.commit()
    cursor.execute("SELECT * FROM p_001_articulo_bienestar ORDER BY id_articulo DESC")
    articulos = cursor.fetchall()
    conn.close()
    return render_template('admin_bienestar.html', articulos=articulos)

# (Las demás rutas CRUD de otros y edición se mantienen intactas tal como pediste)
@app.route('/admin/bienestar/editar/<int:id>', methods=['GET', 'POST'])
def editar_bienestar(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("UPDATE p_001_articulo_bienestar SET titulo=%s, contenido=%s WHERE id_articulo=%s", (request.form['titulo'], request.form['contenido'], id))
        conn.commit()
        return redirect(url_for('admin_bienestar'))
    cursor.execute("SELECT * FROM p_001_articulo_bienestar WHERE id_articulo = %s", (id,))
    articulo = cursor.fetchone()
    conn.close()
    return render_template('editar_bienestar.html', articulo=articulo)

@app.route('/admin/bienestar/eliminar/<int:id>')
def eliminar_bienestar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM p_001_articulo_bienestar WHERE id_articulo = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_bienestar'))

@app.route('/admin/otros', methods=['GET', 'POST'])
def admin_otros():
    if session.get('user_rol') != 1: return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        tipo = request.form.get('tipo_registro')
        if tipo == 'deporte':
            cursor.execute("INSERT INTO p_001_actividad_deportiva (nombre_taller, precio, id_comuna) VALUES (%s, %s, %s)",
                            (request.form['nombre'], request.form['precio'], request.form['id_comuna']))
        elif tipo == 'academia':
            gratuidad = 1 if request.form.get('gratuidad') else 0
            cursor.execute("INSERT INTO p_001_carrera (nom_carrera, tiene_gratuidad, id_institucion) VALUES (%s, %s, %s)",
                            (request.form['nombre'], gratuidad, request.form['id_institucion']))
        conn.commit()
    
    cursor.execute("SELECT a.*, c.nombre_comuna FROM p_001_actividad_deportiva a JOIN p_001_comuna c ON a.id_comuna = c.id_comuna")
    actividades = cursor.fetchall()
    cursor.execute("SELECT c.*, i.nombre_inst FROM p_001_carrera c JOIN p_001_institucion i ON c.id_institucion = i.id_institucion")
    carreras = cursor.fetchall()
    cursor.execute("SELECT * FROM p_001_comuna ORDER BY nombre_comuna")
    comunas = cursor.fetchall()
    cursor.execute("SELECT * FROM p_001_institucion WHERE tipo_institucion = 'academia'")
    inst_academia = cursor.fetchall()
    conn.close()
    return render_template('admin_otros.html', actividades=actividades, carreras=carreras, comunas=comunas, inst_academia=inst_academia)

# (Rutas de editar deportes y academia se mantienen)
@app.route('/admin/deportes/editar/<int:id>', methods=['GET', 'POST'])
def editar_deporte(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute("UPDATE p_001_actividad_deportiva SET nombre_taller=%s, precio=%s, id_comuna=%s WHERE id_actividad=%s", (request.form['nombre'], request.form['precio'], request.form['id_comuna'], id))
        conn.commit()
        return redirect(url_for('admin_otros'))
    cursor.execute("SELECT * FROM p_001_actividad_deportiva WHERE id_actividad = %s", (id,))
    deporte = cursor.fetchone()
    cursor.execute("SELECT * FROM p_001_comuna")
    comunas = cursor.fetchall()
    conn.close()
    return render_template('editar_deporte.html', deporte=deporte, comunas=comunas)

@app.route('/admin/deportes/eliminar/<int:id>')
def eliminar_deporte(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM p_001_actividad_deportiva WHERE id_actividad = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_otros'))

@app.route('/admin/academia/editar/<int:id>', methods=['GET', 'POST'])
def editar_carrera(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        gratuidad = 1 if request.form.get('gratuidad') else 0
        cursor.execute("UPDATE p_001_carrera SET nom_carrera=%s, tiene_gratuidad=%s, id_institucion=%s WHERE id_carrera=%s", (request.form['nombre'], gratuidad, request.form['id_institucion'], id))
        conn.commit()
        return redirect(url_for('admin_otros'))
    cursor.execute("SELECT * FROM p_001_carrera WHERE id_carrera = %s", (id,))
    carrera = cursor.fetchone()
    cursor.execute("SELECT * FROM p_001_institucion WHERE tipo_institucion = 'academia'")
    instituciones = cursor.fetchall()
    conn.close()
    return render_template('editar_carrera.html', carrera=carrera, instituciones=instituciones)

@app.route('/admin/academia/eliminar/<int:id>')
def eliminar_carrera(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM p_001_carrera WHERE id_carrera = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_otros'))

# --- ACCESO (ESTA ES LA PARTE CLAVE CORREGIDA) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, password_input = request.form['email'], request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Solo buscamos por email
        cursor.execute("SELECT * FROM p_001_usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        # Verificamos si el usuario existe y si el hash coincide con lo ingresado
        if user and check_password_hash(user['password_hash'], password_input):
            session.update({
                'user_id': user['id_usuario'], 
                'user_name': user['nombre_completo'], 
                'user_rol': user['id_rol']
            })
            return redirect(url_for('admin_panel') if user['id_rol'] == 1 else url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)