import os

# MongoDB URI - usar variable de entorno o valor por defecto
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cona_inv')