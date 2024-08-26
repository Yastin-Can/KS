import sys
import os
import uuid
import qrcode
import pymysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, session, sessions, jsonify
from user import Usuario
from config.db import connectToMySQL
from product import Producto, Categoria


app = Flask(__name__, static_folder='../web', template_folder='../web')
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K' 



@app.route('/')
def index():
    num_imagenes = 1
    return render_template('main.html', num_imagenes=num_imagenes, active_page='index')


@app.route('/productos')
def product():
    return render_template('product.html', active_page='product')

@app.route('/name-user/productos')


@app.route('/name-user/productos')
def compras():
    if 'username' in session:
        username = session['username']
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        data = (username,)
        try:
            db = connectToMySQL('kiosco_saludable')
            result = db.query_db(query, data)
            if result:
                user = Usuario(result[0])
                categorias = Categoria.get_all()
                productos = Producto.get_all()
                return render_template('user-product.html', user=user, categorias=categorias, productos=productos, active_page='compras')
            else:
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/name-user/productos/<int:categoria_id>')
def compras_por_categoria(categoria_id):
    if 'username' in session:
        username = session['username']
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        data = (username,)
        try:
            db = connectToMySQL('kiosco_saludable')
            result = db.query_db(query, data)
            if result:
                user = Usuario(result[0])
                categorias = Categoria.get_all()
                productos = Producto.get_by_category(categoria_id)
                return render_template('user-product.html', user=user, categorias=categorias, productos=productos, active_page='compras')
            else:
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/contactanos')
def contact():
    return render_template('contact.html', active_page='contact')

@app.route('/name-user/contactanos')
def contacto():
    if 'username' in session:
        username = session['username']
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        data = (username,)
        try:
            db = connectToMySQL('kiosco_saludable')
            result = db.query_db(query, data)
            if result:
                user = Usuario(result[0])
                return render_template('user-contact.html', user=user)
            else:
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/login-register')
def cuenta():
    users = Usuario.get_all()
    if users is False:
        return 'Error al obtener usuarios de la base de datos'
    print(users)
    return render_template('login-register.html', active_page='cuenta')

@app.route('/name-user')
def index_user():
    if 'username' in session:
        username = session['username']
        # Obtener el usuario de la base de datos usando su nombre
        query = "SELECT * FROM usuarios WHERE nombre = %s"
        data = (username,)
        try:
            db = connectToMySQL('kiosco_saludable')
            result = db.query_db(query, data)
            if result:
                user = Usuario(result[0])  # Suponiendo que hay un solo resultado
                return render_template('main-user.html', user=user)
            else:
                return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre']
    email = request.form['email']
    contraseña = request.form['pswd']
    codigo_qr = str(uuid.uuid4())
    fto_perfil = 'default.png'
    ps = 0


    query = """
    INSERT INTO usuarios (nombre, ps, email, contraseña, codigo_qr, fto_perfil)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    data = (nombre, ps, email, contraseña, codigo_qr, fto_perfil)

    try:
        db = connectToMySQL('kiosco_saludable')
        result = db.query_db(query, data)
        if result:
            generate_qr_code(codigo_qr)
            session['username'] = nombre  # Iniciar sesión automáticamente
            return redirect(url_for('index_user'))
        else:
            return 'Error al registrar el usuario'
    except Exception as e:
        print(f"Error: {e}")
        return f'Error al registrar el usuario: {e}'
    
    
base_dir = os.path.abspath(os.path.dirname(__file__))
qr_dir = os.path.join(base_dir, '..', 'web', 'img', 'qr')

base_dir = os.path.abspath(os.path.dirname(__file__))
qr_dir = os.path.join(base_dir, '..', 'web', 'img', 'qr')

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
    img_path = os.path.join(qr_dir, f'{codigo_qr}.png')  # Usa la ruta absoluta aquí
    img.save(img_path)





@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    contraseña = request.form['pswd']
    query = "SELECT * FROM usuarios WHERE email = %s AND contraseña = %s"
    data = (email, contraseña)

    try:
        db = connectToMySQL('kiosco_saludable')
        result = db.query_db(query, data)
        if result:
            session['username'] = result[0]['nombre']
            return redirect(url_for('index_user'))
        else:
            return 'Credenciales incorrectas'
    except Exception as e:
        print(f"Error: {e}")
        return f'Error al iniciar sesión: {e}'
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))




def get_db_connection():
    connection = connectToMySQL('kiosco_saludable')
    cursor = connection.cursor()
    return connection, cursor



@app.route('/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    data = request.form
    producto_id = data['producto_id']
    query = "SELECT * FROM productos WHERE id = %s"
    product_id = (producto_id,)
    try:
        connection, cursor = get_db_connection()
        cursor.execute(query, product_id)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            carrito = session.get('carrito_items', [])
            carrito.append(result)
            session['carrito'] = carrito
            return jsonify({"message": "Producto añadido al carrito"}), 200
        else:
            return jsonify({"message": "Producto no encontrado"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"Error al agregar el producto al carrito: {e}"}), 500


@app.route('/confirmar-compra', methods=['POST'])
def confirmar_compra():
    if 'username' in session:
        username = session['username']
        carrito = session.get('carrito', [])
        if not carrito:
            return jsonify({"message": "El carrito está vacío"}), 400
        try:
            
            session['carrito'] = []
            return jsonify({"message": "Compra confirmada"}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": f"Error al confirmar la compra: {e}"}), 500
    else:
        return jsonify({"message": "Usuario no autenticado"}), 401


app.secret_key = b'my_super_secret_key'


if __name__ == '__main__':
    app.run(debug=True)