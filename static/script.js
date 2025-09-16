// Toast notification system
function showToast(message, type = 'info', duration = 4000) {
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
                <strong class="me-auto"></strong>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 4000 });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    container.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999;';
    document.body.appendChild(container);
    return container;
}

// User management functions
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

// Parish management functions
function editParroquia(id, nombre, canton, codigo) {
    document.getElementById('edit_parroquia_id').value = id;
    document.getElementById('edit_nombre').value = nombre;
    document.getElementById('edit_canton').value = canton;
    document.getElementById('edit_codigo').value = codigo;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

// Assignment management functions
function editAsignacion(id, responsable, observaciones) {
    document.getElementById('edit_asignacion_id').value = id;
    document.getElementById('edit_responsable').value = responsable;
    document.getElementById('edit_observaciones').value = observaciones;
    new bootstrap.Modal(document.getElementById('editModal')).show();
}

// Inventory management functions
function toggleOtroTipo() {
    const tipoSelect = document.getElementById('tipoSelect');
    const otroTipoDiv = document.getElementById('otroTipoDiv');
    
    if (tipoSelect && otroTipoDiv) {
        if (tipoSelect.value === 'Otro') {
            otroTipoDiv.style.display = 'block';
        } else {
            otroTipoDiv.style.display = 'none';
        }
    }
}

// Role selection handlers
document.addEventListener('DOMContentLoaded', function() {
    // Role select for user creation
    const roleSelect = document.getElementById('roleSelect');
    if (roleSelect) {
        roleSelect.addEventListener('change', function() {
            const parroquiaDiv = document.getElementById('parroquiaSelect');
            if (parroquiaDiv) {
                if (this.value === 'admin_parroquia' || this.value === 'tecnico') {
                    parroquiaDiv.style.display = 'block';
                } else {
                    parroquiaDiv.style.display = 'none';
                }
            }
        });
    }

    // Role select for user editing
    const editRoleSelect = document.getElementById('edit_role');
    if (editRoleSelect) {
        editRoleSelect.addEventListener('change', function() {
            const parroquiaDiv = document.getElementById('editParroquiaSelect');
            if (parroquiaDiv) {
                if (this.value === 'admin_parroquia' || this.value === 'tecnico') {
                    parroquiaDiv.style.display = 'block';
                } else {
                    parroquiaDiv.style.display = 'none';
                }
            }
        });
    }

    // Tipo select for inventory
    const tipoSelect = document.getElementById('tipoSelect');
    if (tipoSelect) {
        tipoSelect.addEventListener('change', toggleOtroTipo);
    }
});