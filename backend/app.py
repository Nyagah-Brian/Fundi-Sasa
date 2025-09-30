# backend/app.py
from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints
from routes.technician import technician_bp
from routes.auth import auth_bp   # we will implement auth routes soon

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Fundi Sasa backend is running!"})

# Register blueprints
app.register_blueprint(technician_bp, url_prefix="/technicians")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
