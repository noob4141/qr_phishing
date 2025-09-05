from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from email_validator import validate_email, EmailNotValidError
from models import db, User   # Import schema
from config import usermail, firstname, lastname  # Default prefill values
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ------------------ Database Config ------------------
# Railway MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://root:EjSkQfSktfpGcdwLCSLwCiJOZHpibTTD"
    "@yamanote.proxy.rlwy.net:32922/railway"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ------------------ Routes ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register_form")
def register_form():
    email = request.args.get("email", usermail)
    fname = request.args.get("firstname", firstname)
    lname = request.args.get("lastname", lastname)

    return render_template("register.html", email=email, firstname=fname, lastname=lname)


@app.route("/submit", methods=["POST"])
def submit():
    """Handle registration form submission"""
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    first_name = (request.form.get("first_name") or "").strip()
    last_name = (request.form.get("last_name") or "").strip()

    # -------- Validation --------
    if not email or not password or not first_name or not last_name:
        flash("All fields are required.", "danger")
        return redirect(url_for("register_form"))

    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError:
        flash("Invalid email address.", "danger")
        return redirect(url_for("register_form"))

    if len(password) < 5:
        flash("Password must be at least 5 characters.", "danger")
        return redirect(url_for("register_form"))

    # -------- Save new user --------
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        Password=password   # ⚠️ ideally hash this with generate_password_hash
    )

    db.session.add(user)
    db.session.commit()

    return render_template("success.html", email=email)


# ------------------ Run ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables exist
    app.run(host="0.0.0.0", port=5000, debug=True)
