# Sistema de Inventario CONA - Gestión Jerárquica por Parroquias

## 📋 Descripción

Sistema de inventario jerárquico diseñado para gestionar bienes tecnológicos en 61 parroquias, con tres niveles de usuarios:

- **Super Administrador**: Controla todo el sistema, gestiona parroquias y usuarios
- **Administradores de Parroquia**: Gestionan inventario y asignación de bienes de su parroquia específica

## 🏗️ Arquitectura del Sistema

```
Super Administrador (1)
├── Administrador Parroquia 1
│   └── Bienes Parroquia 1
├── Administrador Parroquia 2
│   └── Bienes Parroquia 2
└── ... (hasta 61 parroquias)
```

## 🚀 Instalación

### Prerrequisitos

1. **Python 3.8+**
2. **MongoDB** (local o remoto)
3. **pip** (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd InventarioCona
```

2. **Instalar dependencias**
```bash
pip install flask flask-login pymongo werkzeug
```

3. **Configurar MongoDB**
   - Instalar MongoDB Community Edition
   - Iniciar el servicio de MongoDB
   - El sistema se conectará automáticamente a `mongodb://localhost:27017/`

4. **Poblar la base de datos**
```bash
python populate_db.py
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

6. **Acceder al sistema**
   - Abrir navegador en: `http://localhost:10000`

## 👥 Credenciales por Defecto

### Super Administrador
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### Administradores de Parroquia
- **Quito**: `admin_quito` / `admin123`
- **Guayaquil**: `admin_guayaquil` / `admin123`
- **Cuenca**: `admin_cuenca` / `admin123`



## 🔧 Funcionalidades por Rol

### Super Administrador
- ✅ Gestionar las 61 parroquias
- ✅ Crear administradores de parroquia
- ✅ Crear técnicos y asignarlos a parroquias
- ✅ Ver estadísticas globales del sistema
- ✅ Control total sobre usuarios y parroquias

### Administrador de Parroquia
- ✅ Gestionar inventario de su parroquia
- ✅ Agregar, editar y eliminar bienes
- ✅ Asignar bienes a técnicos de su parroquia
- ✅ Controlar devolución de bienes
- ✅ Ver estadísticas de su parroquia

### Técnico
- ✅ Ver bienes asignados personalmente
- ✅ Consultar detalles de sus equipos
- ✅ Ver información de su parroquia
- ✅ Dashboard personalizado

## 📊 Estructura de la Base de Datos

### Colecciones MongoDB

1. **users**: Usuarios del sistema
   ```json
   {
     "username": "string",
     "password": "hash",
     "role": "super_admin|admin_parroquia|tecnico",
     "nombre": "string",
     "apellido": "string",
     "email": "string",
     "parroquia_id": "ObjectId",
     "created_at": "datetime"
   }
   ```

2. **parroquias**: Información de parroquias
   ```json
   {
     "nombre": "string",
     "canton": "string",
     "codigo": "string",
     "created_at": "datetime"
   }
   ```

3. **inventarios**: Bienes por parroquia
   ```json
   {
     "codigo": "string",
     "nombre": "string",
     "tipo": "string",
     "marca": "string",
     "modelo": "string",
     "estado": "disponible|asignado|en_mantenimiento|dañado",
     "descripcion": "string",
     "parroquia_id": "ObjectId",
     "created_at": "datetime"
   }
   ```

4. **bienes_asignados**: Control de asignaciones
   ```json
   {
     "bien_id": "ObjectId",
     "tecnico_id": "ObjectId",
     "parroquia_id": "ObjectId",
     "fecha_asignacion": "datetime",
     "fecha_devolucion": "datetime",
     "observaciones": "string",
     "estado": "activo|devuelto",
     "created_at": "datetime"
   }
   ```

## 🎯 Casos de Uso

### 1. Crear Nueva Parroquia
1. Super admin accede al sistema
2. Va a "Gestionar Parroquias"
3. Completa formulario con datos de la parroquia
4. Sistema asigna código único

### 2. Asignar Administrador a Parroquia
1. Super admin va a "Gestionar Usuarios"
2. Crea usuario con rol "Administrador de Parroquia"
3. Selecciona parroquia específica
4. Usuario puede acceder y gestionar solo su parroquia

### 3. Gestionar Inventario por Parroquia
1. Admin de parroquia accede a su dashboard
2. Va a "Gestionar Inventario"
3. Agrega bienes con códigos únicos
4. Bienes quedan disponibles para asignación

### 4. Asignar Bien a Técnico
1. Admin de parroquia va a "Asignar Bienes"
2. Selecciona bien disponible y técnico
3. Registra fecha y observaciones
4. Bien cambia a estado "asignado"

## 🔒 Seguridad

- ✅ Autenticación por roles
- ✅ Control de acceso por parroquia
- ✅ Passwords hasheados con Werkzeug
- ✅ Validación de formularios
- ✅ Protección CSRF con Flask

## 📱 Responsive Design

- ✅ Compatible con dispositivos móviles
- ✅ Bootstrap 5 para UI responsiva
- ✅ Tablas adaptables
- ✅ Navegación optimizada

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5
- **Iconos**: Font Awesome 6
- **Autenticación**: Flask-Login

## 📈 Escalabilidad

El sistema está diseñado para:
- ✅ Manejar 61+ parroquias
- ✅ Miles de bienes por parroquia
- ✅ Cientos de técnicos
- ✅ Múltiples administradores por parroquia (futuro)
- ✅ Reportes y estadísticas (futuro)

## 🔄 Próximas Mejoras

- [ ] Reportes en PDF/Excel
- [ ] Notificaciones por email
- [ ] Historial de movimientos
- [ ] API REST para integración
- [ ] Dashboard con gráficos
- [ ] Backup automático
- [ ] Logs de auditoría

## 🐛 Solución de Problemas

### Error de Conexión MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
mongod --version
# Iniciar MongoDB si no está activo
mongod
```

### Puerto en Uso
```bash
# Cambiar puerto en app.py línea final
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Dependencias Faltantes
```bash
pip install -r requirements.txt
```

## 📞 Soporte

Para soporte técnico o consultas:
- Email: soporte@cona.gov.ec
- Documentación: Este README
- Issues: Reportar en el repositorio

---

**Desarrollado para CONA - Sistema de Gestión de Inventario Jerárquico**"# inv_cona" 
