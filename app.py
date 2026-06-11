from flask import Flask, render_template, redirect, session
from models import db
from flask_migrate import Migrate
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# 🔐 Secret key
app.config['SECRET_KEY'] = 'secret123'

# 📦 FIXED DB PATH (VERY IMPORTANT)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "careerpilot.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔥 INIT
db.init_app(app)
migrate = Migrate(app, db)

# 🚫 REMOVE create_all() (IMPORTANT)

from routes.auth import auth_bp
from routes.jobs import jobs_bp

app.register_blueprint(auth_bp)
app.register_blueprint(jobs_bp)

@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")

with app.app_context():
    db.create_all()

@app.route("/test")
def test():
     return "WORKING"

if __name__ == "__main__":
    app.run(debug=True)

   