from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import os
import bcrypt
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import logging
from functools import wraps
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
import qrcode
from PIL import Image

app = Flask(__name__)
app.secret_key = 'a1eb8b7d4c7a96ea202923296486a51c'

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
    
    if request.method == 'POST':
        if 'create_user' in request.form:
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_data = {
                'username': username,
                'password': hashed_password,
                'nombre': request.form['nombre'],
                'apellido': request.form['apellido'],
                'email': request.form['email'],
                'role': request.form['role'],
                'created_at': datetime.now()
            }
            if request.form['role'] in ['admin_parroquia', 'tecnico']:
                user_data['parroquia_id'] = ObjectId(request.form['parroquia_id'])
            
            users.insert_one(user_data)
            log_action('CREATE_USER', f'Usuario creado: {username} con rol {user_data["role"]}')
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('super_admin', section='usuarios'))
        
        elif 'create_parroquia' in request.form:
            parroquia_data = {
                'nombre': request.form['nombre'],
                'canton': request.form['canton'],
                'codigo': request.form['codigo'],
                'created_at': datetime.now()
            }
            parroquias.insert_one(parroquia_data)
            flash('Parroquia creada exitosamente', 'success')
            return redirect(url_for('super_admin', section='parroquias'))
        
        elif 'edit_parroquia' in request.form:
            parroquia_id = request.form['parroquia_id']
            parroquias.update_one({'_id': ObjectId(parroquia_id)}, {
                '$set': {
                    'nombre': request.form['edit_nombre'],
                    'canton': request.form['edit_canton'],
                    'codigo': request.form['edit_codigo']
                }
            })
            flash('Parroquia actualizada exitosamente', 'success')
            return redirect(url_for('super_admin', section='parroquias'))
        
        elif 'delete_parroquia' in request.form:
            parroquia_id = request.form['parroquia_id']
            parroquias.delete_one({'_id': ObjectId(parroquia_id)})
            flash('Parroquia eliminada exitosamente', 'success')
            return redirect(url_for('super_admin', section='parroquias'))
        
        elif 'edit_user' in request.form:
            user_id = request.form['user_id']
            update_data = {
                'nombre': request.form['edit_nombre'],
                'apellido': request.form['edit_apellido'],
                'username': request.form['edit_username'],
                'email': request.form['edit_email'],
                'role': request.form['edit_role']
            }
            if request.form.get('edit_password'):
                hashed_password = bcrypt.hashpw(request.form['edit_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_data['password'] = hashed_password
            if request.form['edit_role'] in ['admin_parroquia', 'tecnico'] and request.form.get('edit_parroquia_id'):
                update_data['parroquia_id'] = ObjectId(request.form['edit_parroquia_id'])
            else:
                update_data['parroquia_id'] = None
            
            users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('super_admin', section='usuarios'))
        
        elif 'delete_user' in request.form:
            user_id = request.form['user_id']
            users.delete_one({'_id': ObjectId(user_id)})
            flash('Usuario eliminado exitosamente', 'success')
            return redirect(url_for('super_admin', section='usuarios'))
    
    stats = {
        'total_parroquias': parroquias.count_documents({}),
        'total_usuarios': users.count_documents({}),
        'total_bienes': inventarios.count_documents({}),
        'bienes_asignados': bienes_asignados.count_documents({'estado': 'activo'}),
        'total_tecnicos': users.count_documents({'role': 'tecnico'})
    }
    
    if section == 'parroquias':
        return render_template('gestionar_parroquias.html', 
                             parroquias=list(parroquias.find()))
    elif section == 'usuarios':
        usuarios_con_parroquia = list(users.aggregate([
            {
                '$lookup': {
                    'from': 'parroquias',
                    'localField': 'parroquia_id',
                    'foreignField': '_id',
                    'as': 'parroquia_info'
                }
            },
            {
                '$addFields': {
                    'parroquia_nombre': {
                        '$cond': {
                            'if': {'$gt': [{'$size': '$parroquia_info'}, 0]},
                            'then': {'$arrayElemAt': ['$parroquia_info.nombre', 0]},
                            'else': None
                        }
                    }
                }
            }
        ]))
        return render_template('gestionar_usuarios.html', 
                             usuarios=usuarios_con_parroquia,
                             parroquias=list(parroquias.find()))
    elif section == 'estadisticas':
        # Estadísticas detalladas
        estadisticas_detalladas = {
            'parroquias_con_bienes': inventarios.distinct('parroquia_id'),
            'bienes_por_estado': {
                'disponibles': inventarios.count_documents({'estado': 'disponible'}),
                'asignados': inventarios.count_documents({'estado': 'asignado'}),
                'mantenimiento': inventarios.count_documents({'estado': 'en_mantenimiento'}),
                'dañados': inventarios.count_documents({'estado': 'dañado'})
            },
            'usuarios_por_rol': {
                'super_admin': users.count_documents({'role': 'super_admin'}),
                'admin_parroquia': users.count_documents({'role': 'admin_parroquia'}),
                'tecnicos': users.count_documents({'role': 'tecnico'})
            },
            'asignaciones_activas': bienes_asignados.count_documents({'estado': 'activo'}),
            'asignaciones_devueltas': bienes_asignados.count_documents({'estado': 'devuelto'})
        }
        
        # Top 5 parroquias con más bienes
        top_parroquias = list(inventarios.aggregate([
            {'$group': {'_id': '$parroquia_id', 'total_bienes': {'$sum': 1}}},
            {'$lookup': {
                'from': 'parroquias',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'parroquia_info'
            }},
            {'$unwind': '$parroquia_info'},
            {'$sort': {'total_bienes': -1}},
            {'$limit': 5}
        ]))
        
        return render_template('estadisticas.html',
                             stats=stats,
                             estadisticas=estadisticas_detalladas,
                             top_parroquias=top_parroquias)
    elif section == 'auditoria':
        # Logs de auditoría
        logs = list(audit_logs.find().sort('timestamp', -1).limit(100))
        return render_template('auditoria.html', logs=logs)
    elif section == 'mantenimiento':
        if request.method == 'POST':
            confirmacion = request.form.get('confirmacion', '')
            accion = request.form.get('accion', '')
            
            if confirmacion.upper() == 'CONFIRMAR LIMPIEZA' and accion:
                if accion == 'limpiar_logs':
                    count = audit_logs.count_documents({})
                    audit_logs.delete_many({})
                    log_action('MAINTENANCE', f'Limpieza de logs de auditoría: {count} registros eliminados')
                    flash(f'Se eliminaron {count} logs de auditoría', 'success')
                
                elif accion == 'limpiar_notificaciones':
                    count = notificaciones.count_documents({})
                    notificaciones.delete_many({})
                    log_action('MAINTENANCE', f'Limpieza de notificaciones: {count} registros eliminados')
                    flash(f'Se eliminaron {count} notificaciones', 'success')
                
                elif accion == 'limpiar_asignaciones_devueltas':
                    count = bienes_asignados.count_documents({'estado': 'devuelto'})
                    bienes_asignados.delete_many({'estado': 'devuelto'})
                    log_action('MAINTENANCE', f'Limpieza de asignaciones devueltas: {count} registros eliminados')
                    flash(f'Se eliminaron {count} asignaciones devueltas', 'success')
                
                elif accion == 'reset_completo':
                    # PELIGROSO: Limpiar todo excepto usuarios y parroquias
                    inventarios_count = inventarios.count_documents({})
                    asignaciones_count = bienes_asignados.count_documents({})
                    logs_count = audit_logs.count_documents({})
                    notif_count = notificaciones.count_documents({})
                    
                    inventarios.delete_many({})
                    bienes_asignados.delete_many({})
                    audit_logs.delete_many({})
                    notificaciones.delete_many({})
                    
                    log_action('MAINTENANCE', f'Reset completo: {inventarios_count} bienes, {asignaciones_count} asignaciones, {logs_count} logs, {notif_count} notificaciones eliminados')
                    flash(f'Reset completo realizado: {inventarios_count + asignaciones_count + logs_count + notif_count} registros eliminados', 'warning')
                
                return redirect(url_for('super_admin', section='mantenimiento'))
            else:
                flash('Confirmación incorrecta. Debe escribir exactamente "CONFIRMAR LIMPIEZA"', 'error')
        
        # Estadísticas para mantenimiento
        stats_mantenimiento = {
            'total_logs': audit_logs.count_documents({}),
            'total_notificaciones': notificaciones.count_documents({}),
            'asignaciones_devueltas': bienes_asignados.count_documents({'estado': 'devuelto'}),
            'logs_antiguos': audit_logs.count_documents({
                'timestamp': {'$lt': datetime.now() - timedelta(days=90)}
            })
        }
        
        return render_template('mantenimiento.html', stats=stats_mantenimiento)
    else:
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
    
    if request.method == 'POST':
        if 'create_tecnico' in request.form and current_user.role == 'admin_parroquia':
            username = request.form['username']
            password = request.form['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            tecnico_data = {
                'username': username,
                'password': hashed_password,
                'nombre': request.form['nombre'],
                'apellido': request.form['apellido'],
                'email': request.form['email'],
                'role': 'tecnico',
                'parroquia_id': ObjectId(current_user.parroquia_id),
                'created_at': datetime.now()
            }
            users.insert_one(tecnico_data)
            flash('Técnico creado exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='tecnicos'))
        
        elif 'edit_tecnico' in request.form and current_user.role == 'admin_parroquia':
            tecnico_id = request.form['tecnico_id']
            update_data = {
                'nombre': request.form['edit_nombre'],
                'apellido': request.form['edit_apellido'],
                'username': request.form['edit_username'],
                'email': request.form['edit_email']
            }
            if request.form.get('edit_password'):
                hashed_password = bcrypt.hashpw(request.form['edit_password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_data['password'] = hashed_password
            
            users.update_one({'_id': ObjectId(tecnico_id)}, {'$set': update_data})
            flash('Técnico actualizado exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='tecnicos'))
        
        elif 'delete_tecnico' in request.form and current_user.role == 'admin_parroquia':
            tecnico_id = request.form['tecnico_id']
            users.delete_one({'_id': ObjectId(tecnico_id)})
            flash('Técnico eliminado exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='tecnicos'))
        
        elif 'add_bien' in request.form and current_user.role == 'admin_parroquia':
            # Manejar tipo personalizado
            tipo = request.form['tipo']
            if tipo == 'Otro' and request.form.get('otro_tipo'):
                tipo = request.form['otro_tipo']
            
            # Manejar imagen
            imagen_base64 = None
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename:
                    imagen_base64 = base64.b64encode(file.read()).decode('utf-8')
            
            bien_data = {
                'codigo': request.form['codigo'],
                'nombre': request.form['nombre'],
                'tipo': tipo,
                'marca': request.form['marca'],
                'modelo': request.form['modelo'],
                'color': request.form.get('color', ''),
                'estado': 'disponible',  # Estado de asignación
                'estado_equipo': request.form['estado_equipo'],  # Estado del equipo
                'descripcion': request.form.get('descripcion', ''),
                'imagen': imagen_base64,
                'parroquia_id': ObjectId(current_user.parroquia_id),
                'created_at': datetime.now()
            }
            inventarios.insert_one(bien_data)
            log_action('CREATE_ASSET', f'Bien creado: {bien_data["codigo"]} - {bien_data["nombre"]}')
            flash('Bien agregado exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='inventario'))
        
        elif 'asignar_bien' in request.form and current_user.role == 'admin_parroquia':
            bien_id = ObjectId(request.form['bien_id'])
            responsable = request.form['responsable']
            
            asignacion = {
                'bien_id': bien_id,
                'responsable': responsable,
                'parroquia_id': ObjectId(current_user.parroquia_id),
                'fecha_asignacion': datetime.now(),
                'observaciones': request.form.get('observaciones', ''),
                'estado': 'activo'
            }
            bienes_asignados.insert_one(asignacion)
            inventarios.update_one({'_id': bien_id}, {'$set': {'estado': 'asignado'}})
            bien_info = inventarios.find_one({'_id': bien_id})
            log_action('ASSIGN_ASSET', f'Bien {bien_info["codigo"]} asignado a {responsable}')
            create_notification(responsable, f'Se te ha asignado el bien: {bien_info["nombre"]} ({bien_info["codigo"]})', 'info')
            flash('Bien asignado exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='asignaciones'))
        
        elif 'devolver_bien' in request.form:
            asignacion_id = ObjectId(request.form['asignacion_id'])
            bien_id = ObjectId(request.form['bien_id'])
            
            bienes_asignados.update_one(
                {'_id': asignacion_id},
                {'$set': {'estado': 'devuelto', 'fecha_devolucion': datetime.now()}}
            )
            inventarios.update_one({'_id': bien_id}, {'$set': {'estado': 'disponible'}})
            flash('Bien devuelto exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='asignaciones'))
        
        elif 'edit_asignacion' in request.form:
            asignacion_id = ObjectId(request.form['asignacion_id'])
            bienes_asignados.update_one(
                {'_id': asignacion_id},
                {'$set': {
                    'responsable': request.form['edit_responsable'],
                    'observaciones': request.form['edit_observaciones']
                }}
            )
            flash('Asignación actualizada exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='asignaciones'))
        
        elif 'delete_asignacion' in request.form:
            asignacion_id = ObjectId(request.form['asignacion_id'])
            bien_id = ObjectId(request.form['bien_id'])
            
            bienes_asignados.delete_one({'_id': asignacion_id})
            inventarios.update_one({'_id': bien_id}, {'$set': {'estado': 'disponible'}})
            flash('Asignación eliminada exitosamente', 'success')
            return redirect(url_for('admin_parroquia', section='asignaciones'))
    
    stats = {
        'total_bienes': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id)}),
        'bienes_disponibles': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'disponible'}),
        'bienes_asignados': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'asignado'}),
        'bienes_mantenimiento': inventarios.count_documents({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'en_mantenimiento'}),
        'total_tecnicos': users.count_documents({'role': 'tecnico', 'parroquia_id': ObjectId(current_user.parroquia_id)})
    }
    
    if section == 'inventario':
        # Filtros de búsqueda
        search = request.args.get('search', '')
        estado_filter = request.args.get('estado', '')
        tipo_filter = request.args.get('tipo', '')
        
        query = {'parroquia_id': ObjectId(current_user.parroquia_id)}
        
        if search:
            query['$or'] = [
                {'codigo': {'$regex': search, '$options': 'i'}},
                {'nombre': {'$regex': search, '$options': 'i'}},
                {'marca': {'$regex': search, '$options': 'i'}},
                {'modelo': {'$regex': search, '$options': 'i'}}
            ]
        
        if estado_filter:
            query['estado'] = estado_filter
            
        if tipo_filter:
            query['tipo'] = tipo_filter
        
        bienes_parroquia = list(inventarios.find(query))
        tipos_disponibles = inventarios.distinct('tipo', {'parroquia_id': ObjectId(current_user.parroquia_id)})
        
        return render_template('gestionar_inventario.html',
                             parroquia=parroquia_info,
                             bienes=bienes_parroquia,
                             tipos_disponibles=tipos_disponibles,
                             search=search,
                             estado_filter=estado_filter,
                             tipo_filter=tipo_filter)
    elif section == 'tecnicos' and current_user.role == 'admin_parroquia':
        tecnicos_parroquia = list(users.find({'role': 'tecnico', 'parroquia_id': ObjectId(current_user.parroquia_id)}))
        return render_template('gestionar_tecnicos.html',
                             parroquia=parroquia_info,
                             tecnicos=tecnicos_parroquia)
    elif section == 'asignaciones' and current_user.role == 'admin_parroquia':
        bienes_disponibles = list(inventarios.find({'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'disponible'}))
        asignaciones_activas = list(bienes_asignados.aggregate([
            {'$match': {'parroquia_id': ObjectId(current_user.parroquia_id), 'estado': 'activo'}},
            {'$lookup': {
                'from': 'inventarios',
                'localField': 'bien_id',
                'foreignField': '_id',
                'as': 'bien_info'
            }},
            {'$unwind': '$bien_info'}
        ]))
        return render_template('gestionar_asignaciones.html',
                             parroquia=parroquia_info,
                             bienes_disponibles=bienes_disponibles,
                             asignaciones=asignaciones_activas)
    elif section == 'estadisticas':
        # Estadísticas de la parroquia
        estadisticas_parroquia = {
            'bienes_por_tipo': list(inventarios.aggregate([
                {'$match': {'parroquia_id': ObjectId(current_user.parroquia_id)}},
                {'$group': {'_id': '$tipo', 'cantidad': {'$sum': 1}}}
            ])),
            'asignaciones_por_mes': list(bienes_asignados.aggregate([
                {'$match': {'parroquia_id': ObjectId(current_user.parroquia_id)}},
                {'$group': {
                    '_id': {
                        'mes': {'$month': '$fecha_asignacion'},
                        'año': {'$year': '$fecha_asignacion'}
                    },
                    'cantidad': {'$sum': 1}
                }},
                {'$sort': {'_id.año': 1, '_id.mes': 1}}
            ])),
            'responsables_activos': bienes_asignados.distinct('responsable', {
                'parroquia_id': ObjectId(current_user.parroquia_id),
                'estado': 'activo'
            })
        }
        
        return render_template('estadisticas_parroquia.html',
                             parroquia=parroquia_info,
                             stats=stats,
                             estadisticas=estadisticas_parroquia)
    elif current_user.role == 'tecnico':
        # Vista para técnicos - solo sus bienes asignados
        bienes_asignados_tecnico = list(bienes_asignados.aggregate([
            {'$match': {
                'responsable': session.get('full_name', current_user.username),
                'estado': 'activo'
            }},
            {'$lookup': {
                'from': 'inventarios',
                'localField': 'bien_id',
                'foreignField': '_id',
                'as': 'bien_info'
            }},
            {'$unwind': '$bien_info'}
        ]))
        return render_template('tecnico_view.html',
                             parroquia=parroquia_info,
                             bienes_asignados=bienes_asignados_tecnico,
                             stats={'bienes_asignados': len(bienes_asignados_tecnico)})
    else:
        return render_template('admin_parroquia.html',
                             parroquia=parroquia_info,
                             stats=stats)



@app.route('/reporte_pdf/<tipo>')
@login_required
def generar_reporte_pdf(tipo):
    if current_user.role not in ['super_admin', 'admin_parroquia']:
        return redirect(url_for('index'))
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    if tipo == 'inventario' and current_user.role == 'admin_parroquia':
        parroquia_info = parroquias.find_one({'_id': ObjectId(current_user.parroquia_id)})
        bienes = list(inventarios.find({'parroquia_id': ObjectId(current_user.parroquia_id)}))
        
        story.append(Paragraph(f"Reporte de Inventario - {parroquia_info['nombre']}", title_style))
        story.append(Spacer(1, 12))
        
        # Tabla de bienes
        data = [['Código', 'Nombre', 'Tipo', 'Marca', 'Modelo', 'Estado']]
        for bien in bienes:
            data.append([
                bien['codigo'],
                bien['nombre'],
                bien['tipo'],
                bien['marca'],
                bien['modelo'],
                bien['estado_equipo']
            ])
        
    elif tipo == 'asignaciones' and current_user.role == 'admin_parroquia':
        parroquia_info = parroquias.find_one({'_id': ObjectId(current_user.parroquia_id)})
        asignaciones = list(bienes_asignados.aggregate([
            {'$match': {'parroquia_id': ObjectId(current_user.parroquia_id)}},
            {'$lookup': {
                'from': 'inventarios',
                'localField': 'bien_id',
                'foreignField': '_id',
                'as': 'bien_info'
            }},
            {'$unwind': '$bien_info'}
        ]))
        
        story.append(Paragraph(f"Reporte de Asignaciones - {parroquia_info['nombre']}", title_style))
        story.append(Spacer(1, 12))
        
        data = [['Código', 'Bien', 'Responsable', 'Fecha', 'Estado']]
        for asig in asignaciones:
            data.append([
                asig['bien_info']['codigo'],
                asig['bien_info']['nombre'],
                asig['responsable'],
                asig['fecha_asignacion'].strftime('%d/%m/%Y'),
                asig['estado']
            ])
    
    elif tipo == 'general' and current_user.role == 'super_admin':
        story.append(Paragraph("Reporte General del Sistema", title_style))
        story.append(Spacer(1, 12))
        
        # Estadísticas generales
        total_parroquias = parroquias.count_documents({})
        total_usuarios = users.count_documents({})
        total_bienes = inventarios.count_documents({})
        
        data = [['Concepto', 'Cantidad']]
        data.append(['Total Parroquias', str(total_parroquias)])
        data.append(['Total Usuarios', str(total_usuarios)])
        data.append(['Total Bienes', str(total_bienes)])
    
    else:
        return "Tipo de reporte no válido", 400
    
    # Crear tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_{tipo}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

@app.route('/exportar_excel/<tipo>')
@login_required
def exportar_excel(tipo):
    if current_user.role not in ['super_admin', 'admin_parroquia']:
        return redirect(url_for('index'))
    
    wb = Workbook()
    ws = wb.active
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    if tipo == 'inventario' and current_user.role == 'admin_parroquia':
        parroquia_info = parroquias.find_one({'_id': ObjectId(current_user.parroquia_id)})
        bienes = list(inventarios.find({'parroquia_id': ObjectId(current_user.parroquia_id)}))
        
        ws.title = f"Inventario {parroquia_info['nombre']}"
        headers = ['Código', 'Nombre', 'Tipo', 'Marca', 'Modelo', 'Color', 'Estado Asignación', 'Estado Equipo', 'Descripción']
        
        # Escribir headers
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
        
        # Escribir datos
        for row, bien in enumerate(bienes, 2):
            ws.cell(row=row, column=1, value=bien['codigo'])
            ws.cell(row=row, column=2, value=bien['nombre'])
            ws.cell(row=row, column=3, value=bien['tipo'])
            ws.cell(row=row, column=4, value=bien['marca'])
            ws.cell(row=row, column=5, value=bien['modelo'])
            ws.cell(row=row, column=6, value=bien.get('color', ''))
            ws.cell(row=row, column=7, value=bien['estado'])
            ws.cell(row=row, column=8, value=bien.get('estado_equipo', ''))
            ws.cell(row=row, column=9, value=bien.get('descripcion', ''))
    
    elif tipo == 'general' and current_user.role == 'super_admin':
        ws.title = "Reporte General"
        headers = ['Parroquia', 'Total Bienes', 'Disponibles', 'Asignados', 'En Mantenimiento']
        
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
        
        parroquias_list = list(parroquias.find())
        for row, parroquia in enumerate(parroquias_list, 2):
            total = inventarios.count_documents({'parroquia_id': parroquia['_id']})
            disponibles = inventarios.count_documents({'parroquia_id': parroquia['_id'], 'estado': 'disponible'})
            asignados = inventarios.count_documents({'parroquia_id': parroquia['_id'], 'estado': 'asignado'})
            mantenimiento = inventarios.count_documents({'parroquia_id': parroquia['_id'], 'estado': 'en_mantenimiento'})
            
            ws.cell(row=row, column=1, value=parroquia['nombre'])
            ws.cell(row=row, column=2, value=total)
            ws.cell(row=row, column=3, value=disponibles)
            ws.cell(row=row, column=4, value=asignados)
            ws.cell(row=row, column=5, value=mantenimiento)
    
    # Ajustar ancho de columnas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Guardar en memoria
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename=reporte_{tipo}_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    return response

@app.route('/generar_qr/<bien_id>')
@login_required
def generar_qr(bien_id):
    if current_user.role not in ['admin_parroquia', 'tecnico']:
        return redirect(url_for('index'))
    
    bien = inventarios.find_one({'_id': ObjectId(bien_id)})
    if not bien:
        return "Bien no encontrado", 404
    
    # Verificar permisos
    if current_user.role == 'admin_parroquia' and str(bien['parroquia_id']) != current_user.parroquia_id:
        return "Sin permisos", 403
    
    # Crear QR con información del bien
    qr_data = f"Código: {bien['codigo']}\nNombre: {bien['nombre']}\nTipo: {bien['tipo']}\nMarca: {bien['marca']}\nModelo: {bien['modelo']}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = f'attachment; filename=qr_{bien["codigo"]}.png'
    
@app.route('/mi_cuenta', methods=['GET', 'POST'])
@login_required
def mi_cuenta():
    user_data = users.find_one({'username': current_user.username})
    if not user_data:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('logout'))
    
    if request.method == 'POST':
        if 'update_profile' in request.form:
            update_data = {
                'nombre': request.form['nombre'],
                'apellido': request.form['apellido'],
                'email': request.form['email']
            }
            
            # Validar cambio de contraseña
            if request.form.get('current_password') or request.form.get('new_password') or request.form.get('confirm_password'):
                current_password = request.form.get('current_password', '')
                new_password = request.form.get('new_password', '')
                confirm_password = request.form.get('confirm_password', '')
                
                if not current_password:
                    flash('Debe ingresar su contraseña actual', 'error')
                    return redirect(url_for('mi_cuenta'))
                
                if not new_password:
                    flash('Debe ingresar la nueva contraseña', 'error')
                    return redirect(url_for('mi_cuenta'))
                
                if new_password != confirm_password:
                    flash('Las nuevas contraseñas no coinciden', 'error')
                    return redirect(url_for('mi_cuenta'))
                
                if len(new_password) < 6:
                    flash('La nueva contraseña debe tener al menos 6 caracteres', 'error')
                    return redirect(url_for('mi_cuenta'))
                
                # Verificar contraseña actual
                if not bcrypt.checkpw(current_password.encode('utf-8'), user_data['password'].encode('utf-8')):
                    flash('La contraseña actual es incorrecta', 'error')
                    return redirect(url_for('mi_cuenta'))
                
                # Cambiar contraseña
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                update_data['password'] = hashed_password
                log_action('CHANGE_PASSWORD', f'Usuario {current_user.username} cambió su contraseña')
                flash('Contraseña cambiada exitosamente', 'success')
            
            users.update_one({'username': current_user.username}, {'$set': update_data})
            session['full_name'] = f"{update_data['nombre']} {update_data['apellido']}".strip()
            log_action('UPDATE_PROFILE', f'Usuario {current_user.username} actualizó su perfil')
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('mi_cuenta'))
    
    # Obtener información de parroquia si aplica
    parroquia_info = None
    if user_data.get('parroquia_id'):
        parroquia_info = parroquias.find_one({'_id': ObjectId(user_data['parroquia_id'])})
    
    # Estadísticas personales
    stats_personales = {}
    if current_user.role == 'admin_parroquia':
        stats_personales = {
            'bienes_gestionados': inventarios.count_documents({'parroquia_id': ObjectId(user_data['parroquia_id'])}),
            'asignaciones_realizadas': bienes_asignados.count_documents({'parroquia_id': ObjectId(user_data['parroquia_id'])}),
            'tecnicos_creados': users.count_documents({'role': 'tecnico', 'parroquia_id': ObjectId(user_data['parroquia_id'])})
        }
    elif current_user.role == 'tecnico':
        stats_personales = {
            'bienes_asignados': bienes_asignados.count_documents({
                'responsable': session.get('full_name', current_user.username),
                'estado': 'activo'
            })
        }
    elif current_user.role == 'super_admin':
        stats_personales = {
            'total_parroquias': parroquias.count_documents({}),
            'total_usuarios': users.count_documents({}),
            'total_bienes': inventarios.count_documents({})
        }
    
    # Actividad reciente del usuario
    actividad_reciente = list(audit_logs.find(
        {'user_id': current_user.username}
    ).sort('timestamp', -1).limit(10))
    
    return render_template('mi_cuenta.html',
                         user_data=user_data,
                         parroquia_info=parroquia_info,
                         stats_personales=stats_personales,
                         actividad_reciente=actividad_reciente)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=True)