from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import os
import bcrypt
import base64
from io import BytesIO
import logging
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'a1eb8b7d4c7a96ea202923296486a51c')

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from config import MONGO_URI
client = MongoClient(MONGO_URI)
cona_inv = client['cona_inv']
users = cona_inv['users']
parroquias = cona_inv['parroquias']
inventarios = cona_inv['inventarios']
bienes_asignados = cona_inv['bienes_asignados']
audit_logs = cona_inv['audit_logs']
notificaciones = cona_inv['notificaciones']

def log_action(action, details, user_id=None):
    """Registrar acciones en el sistema de auditoría"""
    try:
        log_entry = {
            'action': action,
            'details': details,
            'user_id': user_id or (current_user.username if current_user.is_authenticated else 'anonymous'),
            'timestamp': datetime.now(),
            'ip_address': request.remote_addr if request else 'unknown'
        }
        audit_logs.insert_one(log_entry)
    except Exception as e:
        print(f"Error logging action: {e}")

def create_notification(user_id, message, tipo='info'):
    """Crear notificación para usuario"""
    try:
        notification = {
            'user_id': user_id,
            'message': message,
            'tipo': tipo,
            'leida': False,
            'timestamp': datetime.now()
        }
        notificaciones.insert_one(notification)
    except Exception as e:
        print(f"Error creating notification: {e}")

class User(UserMixin):
    def __init__(self, username, role, parroquia_id=None):
        self.id = username 
        self.username = username
        self.role = role
        self.parroquia_id = parroquia_id

@login_manager.user_loader
def load_user(username):
    user_data = users.find_one({'username': username})
    if user_data:
        return User(username=user_data['username'], role=user_data['role'], parroquia_id=user_data.get('parroquia_id'))
    return None

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'super_admin':
            return redirect(url_for('super_admin'))
        elif current_user.role == 'admin_parroquia':
            return redirect(url_for('admin_parroquia'))
        elif current_user.role == 'tecnico':
            return redirect(url_for('admin_parroquia'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            user_obj = User(username=user['username'], role=user['role'], parroquia_id=user.get('parroquia_id'))
            login_user(user_obj)
            session['full_name'] = f"{user.get('nombre', '')} {user.get('apellido', '')}".strip() or username
            log_action('LOGIN', f'Usuario {username} inició sesión', username)
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/super_admin')
@app.route('/super_admin/<section>', methods=['GET', 'POST'])
@login_required
def super_admin(section=None):
    if current_user.role != 'super_admin':
        return redirect(url_for('index'))
    
    # Lógica simplificada del super admin
    stats = {
        'total_parroquias': parroquias.count_documents({}),
        'total_usuarios': users.count_documents({}),
        'total_bienes': inventarios.count_documents({}),
        'bienes_asignados': bienes_asignados.count_documents({'estado': 'activo'}),
        'total_tecnicos': users.count_documents({'role': 'tecnico'})
    }
    
    return render_template('super_admin.html', stats=stats)

@app.route('/admin_parroquia')
@app.route('/admin_parroquia/<section>', methods=['GET', 'POST'])
@login_required
def admin_parroquia(section=None):
    if current_user.role not in ['admin_parroquia', 'tecnico']:
        return redirect(url_for('index'))
    
    parroquia_info = parroquias.find_one({'_id': ObjectId(current_user.parroquia_id)})
    if not parroquia_info:
        flash('Parroquia no encontrada', 'error')
        return redirect(url_for('logout'))
    
    stats = {
        'total_bienes': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id)}),
        'bienes_disponibles': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'disponible'}),
        'bienes_asignados': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'asignado'}),
        'bienes_mantenimiento': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'en_mantenimiento'}),
        'total_tecnicos': users.count_documents({'role': 'tecnico', 'parroquia_id': ObjectId(current_user.parroquia_id)})
    }
    
    return render_template('admin_parroquia.html', parroquia=parroquia_info, stats=stats)

# Rutas deshabilitadas temporalmente
@app.route('/reporte_pdf/<tipo>')
@login_required
def generar_reporte_pdf(tipo):
    flash('Función de reportes PDF temporalmente deshabilitada', 'warning')
    return redirect(url_for('index'))

@app.route('/exportar_excel/<tipo>')
@login_required
def exportar_excel(tipo):
    flash('Función de exportar Excel temporalmente deshabilitada', 'warning')
    return redirect(url_for('index'))

@app.route('/generar_qr/<bien_id>')
@login_required
def generar_qr(bien_id):
    flash('Función de generar QR temporalmente deshabilitada', 'warning')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)