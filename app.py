from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import users_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

# Ruta para autenticar a un usuario y generar un token
@app.route('/login', methods=['POST'])
def login():
    
    # Obtenemos los datos de la solitud
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Verificamos
    if username in users_db and users_db[username]['password'] == password:
        # Crear el token de acceso
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Usuario o contraseña incorrectos"), 401

# Ruta protegida 
@app.route('/protected', methods=['GET'])
@jwt_required() 
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
