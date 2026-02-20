from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME ---------------- #
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ---------------- #
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect("/register")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return redirect("/register")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect("/register")

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect("/register")

    return render_template("register.html")


# ---------------- LOGIN ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Both fields are required!", "danger")
            return redirect("/login")

        user = User.query.filter_by(email=email).first()

        if not user or user.password != password:
            flash("Invalid email or password", "danger")
            return redirect("/login")

        flash("Login successful!", "success")
        return redirect("/")

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)