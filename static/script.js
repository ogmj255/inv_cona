// Sistema de notificaciones Toast - Solo una notificación a la vez
let currentToast = null;

function showToast(message, type = 'info', duration = 4000) {
    // Remover toast anterior si existe
    if (currentToast) {
        currentToast.remove();
        currentToast = null;
    }
    
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const iconMap = {
        'success': 'fa-check-circle text-success',
        'error': 'fa-exclamation-circle text-danger',
        'warning': 'fa-exclamation-triangle text-warning',
        'info': 'fa-info-circle text-info'
    };
    
    const bgMap = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    };
    
    const toastHTML = `
        <div class="toast" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${bgMap[type]} text-white">
                <i class="fas ${iconMap[type]} me-2"></i>
                <strong class="me-auto">Sistema CONA</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    currentToast = toastElement;
    
    const toast = new bootstrap.Toast(toastElement, { delay: Math.min(duration, 4000) });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
        if (currentToast === toastElement) {
            currentToast = null;
        }
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999;';
    document.body.appendChild(container);
    return container;
}

// Gestión de usuarios
function editUsuario(id, nombre, apellido, username, email, role, parroquia_id) {
    document.getElementById('edit_user_id').value = id;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_apellido').value = apellido;
    document.getElementById('edit_username').value = username;
    document.getElementById('edit_email').value = email;
    document.getElementById('edit_role').value = role;
    
    const parroquiaDiv = document.getElementById('editParroquiaSelect');
    if (role === 'admin_parroquia' || role === 'tecnico') {
        parroquiaDiv.style.display = 'block';
        if (parroquia_id) {
            document.getElementById('edit_parroquia_id').value = parroquia_id;
        }
    } else {
        parroquiaDiv.style.display = 'none';
    }
    
    new bootstrap.Modal(document.getElementById('editUserModal')).show();
}

// Gestión de parroquias
function editParroquia(id, nombre, canton, codigo) {
    document.getElementById('edit_parroquia_id').value = id;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_canton').value = canton;
    document.getElementById('edit_codigo').value = codigo;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

// Gestión de asignaciones
function editAsignacion(id, responsable, observaciones) {
    document.getElementById('edit_asignacion_id').value = id;
    document.getElementById('edit_responsable').value = responsable;
    document.getElementById('edit_observaciones').value = observaciones;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

// Gestión de técnicos
function editTecnico(id, nombre, apellido, username, email) {
    document.getElementById('edit_tecnico_id').value = id;
    document.getElementById('edit_tecnico_nombre').value = nombre;
    document.getElementById('edit_tecnico_apellido').value = apellido;
    document.getElementById('edit_tecnico_username').value = username;
    document.getElementById('edit_tecnico_email').value = email;
    new bootstrap.Modal(document.getElementById('editTecnicoModal')).show();
}

// Gestión de bienes
function editBien(id, codigo, nombre, tipo, marca, modelo, descripcion = '') {
    document.getElementById('edit_bien_id').value = id;
    document.getElementById('edit_bien_codigo').value = codigo;
    document.getElementById('edit_bien_nombre').value = nombre;
    document.getElementById('edit_bien_tipo').value = tipo;
    document.getElementById('edit_bien_marca').value = marca;
    document.getElementById('edit_bien_modelo').value = modelo;
    document.getElementById('edit_bien_descripcion').value = descripcion;
    new bootstrap.Modal(document.getElementById('editBienModal')).show();
}

// Alternar tipo "Otro" en inventario
function toggleOtroTipo() {
    const tipoSelect = document.getElementById('tipoSelect');
    const otroTipoDiv = document.getElementById('otroTipoDiv');
    
    if (tipoSelect && otroTipoDiv) {
        otroTipoDiv.style.display = tipoSelect.value === 'Otro' ? 'block' : 'none';
    }
}

// Mostrar modal de imagen
function showImageModal(src, title) {
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('imageModalTitle');
    if (modalImage && modalTitle) {
        modalImage.src = src;
        modalTitle.textContent = title;
        new bootstrap.Modal(document.getElementById('imageModal')).show();
    }
}

// Gestión de asignaciones
const AssignmentManager = {
    returnBien: function(bienId, asignacionId = null) {
        if (confirm('¿Está seguro de devolver este bien?')) {
            const form = document.createElement('form');
            form.method = 'POST';
            const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || '';
            form.innerHTML = `
                <input type="hidden" name="csrf_token" value="${csrfToken}">
                <input type="hidden" name="bien_id" value="${bienId}">
                ${asignacionId ? `<input type="hidden" name="asignacion_id" value="${asignacionId}">` : ''}
                <input type="hidden" name="devolver_bien" value="1">
            `;
            document.body.appendChild(form);
            form.submit();
        }
    }
};

// Función para cambiar estado de bienes
function cambiarEstado(bienId, nuevoEstado) {
    const estadoTexto = nuevoEstado.replace('_', ' ').replace('dañado', 'dañado');
    const iconos = {
        'disponible': '✅',
        'asignado': '🔄', 
        'en_mantenimiento': '🔧',
        'dañado': '❌'
    };
    
    if (confirm(`${iconos[nuevoEstado] || '🔄'} ¿Cambiar estado a: ${estadoTexto}?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/cambiar_estado_bien';
        const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || '';
        form.innerHTML = `
            <input type="hidden" name="csrf_token" value="${csrfToken}">
            <input type="hidden" name="bien_id" value="${bienId}">
            <input type="hidden" name="nuevo_estado" value="${nuevoEstado}">
        `;
        document.body.appendChild(form);
        form.submit();
    }
}

// Gestión de inventario
const InventoryManager = {
    viewHistory: function(bienId) {
        showToast('Función de historial en desarrollo', 'info');
    }
};

// Confirmaciones de mantenimiento
function confirmarAccion(accion) {
    const acciones = {
        'limpiar_logs': '📋 Limpiar Logs de Auditoría',
        'limpiar_notificaciones': '🔔 Limpiar Notificaciones', 
        'limpiar_asignaciones_devueltas': '↩️ Limpiar Asignaciones Devueltas',
        'limpiar_usuarios': '👥 Eliminar TODOS los Usuarios'
    };
    
    const textoAccion = acciones[accion] || accion;
    return confirm(`⚠️ ¿Está seguro de: ${textoAccion}?\n\n🚨 Esta acción no se puede deshacer.`);
}

// Validación de archivos de carga masiva
function validateUploadFile(input) {
    const file = input.files[0];
    if (!file) return true;
    
    const allowedTypes = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                         'application/vnd.ms-excel', 'text/csv'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Tipo de archivo no válido. Solo se permiten archivos Excel o CSV.', 'error');
        input.value = '';
        return false;
    }
    
    if (file.size > maxSize) {
        showToast('El archivo es demasiado grande. Máximo 10MB.', 'error');
        input.value = '';
        return false;
    }
    
    return true;
}

function confirmarResetCompleto() {
    if (!confirm('🚨 ¿ESTÁ ABSOLUTAMENTE SEGURO de realizar un RESET COMPLETO?\n\nEsto eliminará TODOS los datos del sistema excepto parroquias.\n\n⚠️ Esta acción NO SE PUEDE DESHACER.')) {
        return false;
    }
    
    return confirm('🔥 ÚLTIMA CONFIRMACIÓN:\n\n¿Realmente desea proceder con el RESET COMPLETO?\n\n💀 Todos los bienes, asignaciones, logs, notificaciones y USUARIOS serán eliminados PERMANENTEMENTE.\n\n🏛️ Solo se conservarán las parroquias.');
}

// Inicialización al cargar el DOM
document.addEventListener('DOMContentLoaded', function() {
    initializeFormHandlers();
    initializeImageEffects();
    initializeTooltips();
    setDefaultDates();
    resetTecnicoForm();
    
    // Initialize charts based on available data
    if (window.estadisticasData) initEstadisticasCharts();
    if (window.chartData) initParroquiaCharts();
    if (window.reportData) initReportCharts();
    
    // Mostrar solo el primer mensaje Flash si existen
    if (window.flashMessages && window.flashMessages.length > 0) {
        const firstMessage = window.flashMessages[0];
        showToast(firstMessage.message, firstMessage.category);
    }
});

// Inicializar manejadores de formularios
function initializeFormHandlers() {
    // Role select para creación de usuarios
    const roleSelect = document.getElementById('roleSelect');
    if (roleSelect) {
        roleSelect.addEventListener('change', toggleParroquiaSelect);
    }

    // Role select para edición de usuarios
    const editRoleSelect = document.getElementById('edit_role');
    if (editRoleSelect) {
        editRoleSelect.addEventListener('change', toggleEditParroquiaSelect);
    }

    // Tipo select para inventario
    const tipoSelect = document.getElementById('tipoSelect');
    if (tipoSelect) {
        tipoSelect.addEventListener('change', toggleOtroTipo);
    }
}

// Alternar selección de parroquia
function toggleParroquiaSelect() {
    const roleSelect = document.getElementById('roleSelect');
    const parroquiaDiv = document.getElementById('parroquiaSelect');
    if (parroquiaDiv && roleSelect) {
        parroquiaDiv.style.display = 
            (roleSelect.value === 'admin_parroquia' || roleSelect.value === 'tecnico') 
            ? 'block' : 'none';
    }
}

// Alternar selección de parroquia en edición
function toggleEditParroquiaSelect() {
    const editRoleSelect = document.getElementById('edit_role');
    const parroquiaDiv = document.getElementById('editParroquiaSelect');
    if (parroquiaDiv && editRoleSelect) {
        parroquiaDiv.style.display = 
            (editRoleSelect.value === 'admin_parroquia' || editRoleSelect.value === 'tecnico') 
            ? 'block' : 'none';
    }
}

// Inicializar efectos de imagen
function initializeImageEffects() {
    const imageContainers = document.querySelectorAll('.image-container');
    imageContainers.forEach(container => {
        const img = container.querySelector('.hover-image');
        const overlay = container.querySelector('.image-overlay');
        
        if (img && overlay) {
            container.addEventListener('mouseenter', () => {
                img.style.transform = 'scale(1.2)';
                overlay.style.display = 'flex';
            });
            
            container.addEventListener('mouseleave', () => {
                img.style.transform = 'scale(1)';
                overlay.style.display = 'none';
            });
        }
    });
}

// Inicializar tooltips de Bootstrap
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Establecer fechas por defecto
function setDefaultDates() {
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[name="fecha_asignacion"]').forEach(input => {
        if (!input.value) input.value = today;
    });
}

// Función global para mostrar mensajes Flash de Flask
function showFlashMessages() {
    // Esta función será llamada desde los templates con los datos específicos
    // Los mensajes se pasan como parámetros desde cada template
}

// Scripts de estadisticas.html - Gráficos Chart.js
function initEstadisticasCharts() {
    // Gráfico de estado de bienes
    const bienesCtx = document.getElementById('bienesChart');
    if (bienesCtx && window.estadisticasData) {
        new Chart(bienesCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Disponibles', 'Asignados', 'En Mantenimiento', 'Dañados'],
                datasets: [{
                    data: [
                        window.estadisticasData.bienes_por_estado.disponibles,
                        window.estadisticasData.bienes_por_estado.asignados,
                        window.estadisticasData.bienes_por_estado.mantenimiento,
                        window.estadisticasData.bienes_por_estado.dañados
                    ],
                    backgroundColor: ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // Gráfico de usuarios por rol
    const usuariosCtx = document.getElementById('usuariosChart');
    if (usuariosCtx && window.estadisticasData) {
        new Chart(usuariosCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Super Administradores', 'Administradores de Parroquia'],
                datasets: [{
                    data: [
                        window.estadisticasData.usuarios_por_rol.super_admin,
                        window.estadisticasData.usuarios_por_rol.admin_parroquia
                    ],
                    backgroundColor: ['#dc3545', '#28a745']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
}

// Charts for estadisticas_parroquia.html
function initParroquiaCharts() {
    if (!window.chartData) return;
    
    // Gráfico de bienes por tipo
    const tiposCtx = document.getElementById('tiposChart');
    if (tiposCtx) {
        new Chart(tiposCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: window.chartData.tiposData.map(item => item.label),
                datasets: [{
                    data: window.chartData.tiposData.map(item => item.value),
                    backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // Gráfico de estado de bienes
    const estadosCtx = document.getElementById('estadosChart');
    if (estadosCtx) {
        new Chart(estadosCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Disponibles', 'Asignados', 'En Mantenimiento'],
                datasets: [{
                    label: 'Cantidad',
                    data: [
                        window.chartData.estadosData.disponibles,
                        window.chartData.estadosData.asignados,
                        window.chartData.estadosData.mantenimiento
                    ],
                    backgroundColor: ['#28a745', '#ffc107', '#17a2b8']
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// Charts for reportes_super.html
function initReportCharts() {
    if (!window.reportData) return;
    
    const estadoCtx = document.getElementById('estadoChart');
    if (estadoCtx) {
        new Chart(estadoCtx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: window.reportData.estadoData.map(item => item._id.replace('_', ' ').toUpperCase()),
                datasets: [{
                    data: window.reportData.estadoData.map(item => item.count),
                    backgroundColor: ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    const tipoCtx = document.getElementById('tipoChart');
    if (tipoCtx) {
        new Chart(tipoCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: window.reportData.tipoData.map(item => item._id),
                datasets: [{
                    data: window.reportData.tipoData.map(item => item.count),
                    backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
}

// Form reset for tecnicos
function resetTecnicoForm() {
    const form = document.getElementById('createTecnicoForm');
    if (form) {
        form.addEventListener('submit', function() {
            setTimeout(() => {
                const hasErrors = document.querySelector('.toast .bg-danger');
                if (!hasErrors) form.reset();
            }, 100);
        });
    }
}

// Export functions
function exportToPDF() {
    showToast('Función de exportar PDF en desarrollo', 'info');
}

function exportToExcel() {
    showToast('Función de exportar Excel en desarrollo', 'info');
}