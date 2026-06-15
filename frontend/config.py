import os

# Intenta leer del .env. Si no lo encuentra, usa la de desarrollo 
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:5001')