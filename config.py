# Configuración de MongoDB Atlas
# Actualiza estas credenciales con las correctas
MONGO_USERNAME = "ogmoscosoj2"
MONGO_PASSWORD = "iG1h0Y8punlFBa89"
MONGO_CLUSTER = "conagoparedbinventario.ecb0dj0.mongodb.net"
MONGO_DATABASE = "cona_inv"

# Cadena de conexión completa
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=conagoparedbinventario"