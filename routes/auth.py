from flask import Blueprint, render_template, request, redirect, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        # 🛑 USER NOT FOUND
        if not user:
            return render_template("login.html", error="User not found")

        # 🔐 PASSWORD CHECK
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Wrong password")

    return render_template("login.html")


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 🚫 CHECK DUPLICATE USER
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="Username already exists")

        # 🔐 HASH PASSWORD
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")