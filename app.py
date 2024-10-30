import sys
import os
import uuid
from flask_bcrypt import Bcrypt
import qrcode

from config import db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models.user import Usuario
from config.db import connectToMySQL
from models.product import Producto, Categoria
from models.carrito import Carrito
from flask_mail import Mail , Message
from flask import flash

app = Flask(__name__, static_folder='./static')
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

bcrypt = Bcrypt(app)


########################
#----- FORMULARIO -----#
########################

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'infokioscosaludable@gmail.com'  # Cambia esto por tu correo
app.config['MAIL_PASSWORD'] = 'KS12345678.'        # Cambia esto por tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'infokioscosaludable@gmail.com'
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)

@app.route("/enviar_comentarios", methods=['POST'])
def enviar_comentarios():
    nombre = request.form['nombre']
    email = request.form['email']
    celular = request.form['celular']
    fecha = request.form['fecha']
    hora = request.form['hora']
    comentario = request.form['comentario']

    # Crear el mensaje de correo
    msg = Message("Nuevo comentario del formulario", 
                  recipients=["infokioscosaludable@gmail.com"])  # Cambia esto por el destinatario
    msg.body = (f"Nombre: {nombre}\n"
                f"Email: {email}\n"
                f"Celular: {celular}\n"
                f"Fecha: {fecha}\n"
                f"Hora: {hora}\n"
                f"Comentario: {comentario}")
    
    # Enviar el correo
    try:
        mail.send(msg)
        print('el correo fue enviado')
        flash('Comentario enviado correctamente!', 'success')
    except Exception as e:
        print('el correo fue enviado')
        flash(f'Ocurrió un error: {e}', 'danger')

    return redirect('/')



###################################
#-------- RUTAS SECCIONES --------#
###################################

@app.route('/')
def index():
    num_imagenes = 1
    user = None
    categorias = Categoria.get_all()
    productos = Producto.get_all()
    session['carrito_items'] = []
    session['precio_final'] = 0
    session['total_ps'] = 0
    item = None

    if 'username' in session:

        username = session['username']
        usuario_id = session.get('id', None)
        if usuario_id is None:
            return redirect(url_for('login'))

        ps = session['ps']
        qr = session['qr']

        item = Carrito.get_by_user(usuario_id)
        carrito_info = Carrito.obtener_items(usuario_id)

        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = session['precio_final'] // 300

        data = {"nombre": username, "ps": ps, "qr": qr, 'usuario_id': usuario_id}
        user = Usuario.get_user_by_name(data)

    return render_template('main-user.html', num_imagenes=num_imagenes, user=user, item = item, productos = productos, categorias = categorias)
       
@app.route('/productos')
def productos():
    categorias = Categoria.get_all()
    productos = Producto.get_all()
    user = None

    if 'username' in session:

        username = session['username']
        usuario_id = session['id']

        user = Usuario.get_user_by_name({"nombre": username})
        item = Carrito.get_by_user(usuario_id)
        
        carrito_info = Carrito.obtener_items(usuario_id)

        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = session['precio_final'] // 300

    else:
        session['carrito_items'] = []
        session['precio_final'] = 0
        session['total_ps'] = 0
        item = None

    return render_template('user-product.html', categorias=categorias, productos=productos, active_page='productos', user=user, item=item)

@app.route('/productos/<int:categoria_id>')
def productos_por_categoria(categoria_id):
    try:
        categorias = Categoria.get_all()
        productos = Producto.get_by_category(categoria_id)
        return render_template('user-product.html', categorias=categorias, productos=productos, active_page='productos')
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('index'))

@app.route('/contactanos')
def contact():
    user = None
    ps = None
    qr = None
    session['carrito_items'] = []
    session['precio_final'] = 0
    session['total_ps'] = 0
    item = None

    if 'username' in session:

        username = session['username']
        usuario_id = session['id']

        ps = session['ps']
        qr = session['qr']

        item = Carrito.get_by_user(usuario_id)
        carrito_info = Carrito.obtener_items(usuario_id)

        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = session['precio_final'] // 300

        data = {"nombre": username, "ps": ps, "qr": qr}

        user = Usuario.get_user_by_name(data)

        

    return render_template('user-contact.html', user=user, item = item)







###################################
#-------- GENERADOR QR    --------#
###################################


    
base_dir = os.path.abspath(os.path.dirname(__file__))
qr_dir = os.path.join(base_dir, 'static', 'img', 'qr')
def generate_qr_code(codigo_qr):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(codigo_qr)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_path = os.path.join(qr_dir, f'{codigo_qr}.png') 
    img.save(img_path)



###################################
#-------- RUTAS CARRITO ----------#
###################################

@app.route('/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    if request.is_json:
        if 'username' not in session:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401

        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)
        usuario_id = session['id']
    else:
        if 'username' not in session:
            return redirect(url_for('login'))
            
        producto_id = request.form.get('producto_id')
        cantidad = 1
        usuario_id = session['id']

    try:
        for _ in range(int(cantidad)):
            Carrito.agregar_producto(usuario_id, producto_id)
        
        carrito_info = Carrito.obtener_items(usuario_id)
        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = carrito_info["total_precio"] // 300

        if request.is_json:
            total_items = sum(item['cantidad'] for item in session['carrito_items'])
            return jsonify({
                'success': True,
                'total_items': total_items,
                'precio_final': session['precio_final'],
                'total_ps': session['total_ps']
            })
        else:
            return redirect(url_for('productos'))

    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 500
        else:
            return redirect(url_for('productos'))

@app.route('/carrito/agregar_desde_descripcion', methods=['POST'])
def agregar_desde_descripcion():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401

    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)  # Por defecto 1 si no se especifica
    usuario_id = session['id']

    try:
        for _ in range(int(cantidad)):
            Carrito.agregar_producto(usuario_id, producto_id)
        
        carrito_info = Carrito.obtener_items(usuario_id)
        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = carrito_info["total_precio"] // 300

        return jsonify({
            'success': True,
            'total_items': carrito_info["total_cantidad"]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@app.route('/carrito/confirmar', methods=['POST'])
def confirmar_compra():
    if 'username' in session:
        usuario_id = session['id']
        carrito_items = Carrito.obtener_items(usuario_id)
        
        if 'carrito_items' not in session or len(session['carrito_items']) == 0:
            return 'Carrito vacío', 400

        for item in carrito_items:
            if isinstance(item, dict) and 'producto_id' in item:
                producto = Producto.get_by_id(item['producto_id'])
                if producto is not None:
                    Producto.update_stock(item['producto_id'], item['cantidad'])
            else:
                print(f"Error: item no es un diccionario o no contiene 'producto_id': {item}")

        usuario = Usuario.get_user_by_name({"nombre": session['username']})

        usuario.ps += int(session['total_ps'])

        query = "UPDATE usuarios SET ps = %(ps)s WHERE id = %(id)s;"
        data = {'ps': usuario.ps, 'id': usuario.id}
        connectToMySQL('kiosco_saludable').query_db(query, data)

        Carrito.vaciar_carrito(usuario_id)
        
        return redirect(url_for('productos'))
    else:
        return redirect(url_for('login'))
    
@app.route('/carrito/actualizar', methods=['POST'])
def actualizar_carrito():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401

    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    usuario_id = session['id']

    try:
        # Actualizar cantidad en el carrito
        Carrito.update_item(producto_id, cantidad)
        
        # Obtener información actualizada del carrito
        carrito_info = Carrito.obtener_items(usuario_id)
        
        # Actualizar la sesión
        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = carrito_info["total_precio"] // 300

        items_actualizados = []
        for item in carrito_info["carrito_items"]:
            items_actualizados.append({
                'producto_id': item['producto_id'],
                'cantidad': item['cantidad'],
                'precio_total': item['total'],
                'puntos': item['total'] // 300
            })

        return jsonify({
            'success': True,
            'carrito': {
                'items': items_actualizados,
                'total_precio': carrito_info["total_precio"],
                'total_ps': carrito_info["total_precio"] // 300
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_del_carrito():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401

    data = request.get_json()
    producto_id = data.get('producto_id')
    usuario_id = session['id']

    try:
        Carrito.delete_item(producto_id)
        
        carrito_info = Carrito.obtener_items(usuario_id)
        
        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = carrito_info["total_precio"] // 300

        return jsonify({
            'success': True,
            'precio_final': session['precio_final'],
            'total_ps': session['total_ps'],
            'total_items': len(session['carrito_items'])
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



###################################
#-------- RUTAS DEL LOGIN --------#
###################################


@app.route('/planes', methods=['GET'])
def planes():
    user = None
    ps = None
    qr = None
    session['carrito_items'] = []
    session['precio_final'] = 0
    session['total_ps'] = 0
    item = None

    if 'username' in session:
        
        username = session['username']
        usuario_id = session['id']

        ps = session['ps']
        qr = session['qr']

        item = Carrito.get_by_user(usuario_id)
        carrito_info = Carrito.obtener_items(usuario_id)

        session['carrito_items'] = carrito_info["carrito_items"]
        session['precio_final'] = carrito_info["total_precio"]
        session['total_ps'] = session['precio_final'] // 300

        data = {"nombre": username, "ps": ps, "qr": qr}

        user = Usuario.get_user_by_name(data)
        

    return render_template('plans-user.html', user=user, item=item)



@app.route('/login-register')
def cuenta():
    users = Usuario.get_all()
    if users is False:
        return 'Error al obtener usuarios de la base de datos'
    print(users)
    return render_template('login-register.html', active_page='cuenta')

    
@app.route('/register', methods=['POST'])
def register():
    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["pswd"]
    password2 = request.form["pswd2"]
    codigo_qr = str(uuid.uuid4())   
    ps = 0

    errors = []

    if not nombre or len(nombre) < 3:
        errors.append("Nombre invalido")

    if not email or len(email) < 3:
        errors.append("email invalido")

    if password != password2:
        errors.append("Las constraseña no coinciden")

    users = Usuario.select_by_email(email)

    if len(users) > 0:
        errors.append("El usuario ya está registrado")

    if len(errors) > 0:
        return render_template("login-register.html", register_errors=errors)
    
    generate_qr_code(codigo_qr)
    session['username'] = nombre 
    session["qr"] = url_for('static', filename=f'img/qr/{codigo_qr}.png')    
    password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Usuario.insert_one(nombre, ps, email, password, codigo_qr, "default.png")           
    return redirect(url_for('index', user = user))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)  
        try:
            email = request.form['email']
            password = request.form['pswd']
        except KeyError as e:
            errors = ["Falta el campo: " + str(e)]
            return render_template("login-register.html", login_errors=errors)

        errors = []

        if not email or not password:
            errors.append("Email y contraseña son requeridos")

        if len(errors) > 0:
            return render_template("login-register.html", login_errors=errors)

        user = Usuario.select_by_email(email)

        if len(user) == 0:
            errors.append("Email no registrado")
            return render_template("login-register.html", login_errors=errors)

        user = user[0] 
        if not bcrypt.check_password_hash(user.contr, password):
            errors.append("Contraseña incorrecta")
            return render_template("login-register.html", login_errors=errors)
        
        session['id'] = user.id  
        session['username'] = user.nombre 
        session['ps'] = user.ps
        session['qr'] = user.qr


        return redirect(url_for('index'))
    else:
        return render_template("login-register.html")

@app.route('/session-delete' , methods=['GET'])
def delete_session():
    session.clear()
    return redirect(url_for('index'))
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = b'my_super_secret_key'


if __name__ == '__main__':
    app.run(debug=True)