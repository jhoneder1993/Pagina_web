import os

# Importing packages
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///usuarios.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Show portfolio of stocks"""    
    # ir a la pagina web nosotros
    return render_template("index.html")


@app.route("/nosotros")
def nosotros():
    """Show portfolio of stocks"""    
    # ir a la pagina web nosotros
    return render_template("nosotros.html")


@app.route("/contactos")
def contactos():
    """Show portfolio of stocks"""    
    # ir a la pagina web nosotros
    return render_template("contactos.html")


@app.route("/servicios")
def servicios():
    """Show portfolio of stocks"""    
    # ir a la pagina web nosotros
    return render_template("servicios.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password (again)", 400)

        # Ensure que las dos contrase??as sean iguales
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("las contrase??as son diferentes", 400)

        # Ensure username exists and password is correct
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 1:
            return apology("el usuario se encuentra registrado ya", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"),
                   generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/newpassword", methods=["GET", "POST"])
@login_required
def newpassword():
    """cambiar la contrase??a"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Verificar que las contrase??as sean correctas
        if not request.form.get("password"):
            return apology("must provide the old password", 403)

        # Ensure password was submitted
        elif not request.form.get("passwordnew"):
            return apology("must provide a new password", 403)

        elif not request.form.get("passwordnew2"):
            return apology("must provide password confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid old password", 403)

        if request.form.get("passwordnew") != request.form.get("passwordnew2"):
            return apology("the password and the confirmation are't iqual", 403)

        # Guardar nueva contrase??a
        db.execute("UPDATE users SET hash=? WHERE id = ?", generate_password_hash(request.form.get("passwordnew"),
                                                                                  method='pbkdf2:sha256', salt_length=8), session["user_id"])
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")
