import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# setup a secret key, required by sessions
app.secret_key = os.environ.get("SESSION_SECRET") or "a secret key"
# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401

    db.create_all()

@app.route('/')
def index():
    """Monitoreo en tiempo real de la neurona temporal"""
    return render_template('live_monitoring.html')

@app.route('/live-monitoring')
def live_monitoring():
    """Monitoreo en tiempo real de la neurona temporal"""
    return render_template('live_monitoring.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Para Gunicorn
application = app
