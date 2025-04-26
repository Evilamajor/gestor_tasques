from flask import Flask
from routes.tasques import tasques_bp

app = Flask(__name__)

# Registre de les rutes definides al mòdul tasques
app.register_blueprint(tasques_bp)

if __name__ == '__main__':
    app.run(debug=True)
