from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging,
)
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import logging

# starting a flask app
app = Flask(__name__)
app.secret_key = "secret123"

# flask-mysql database connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password_here"
app.config["MYSQL_DB"] = "articletter"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# mysql initialization
mysql = MySQL(app)

# articles from data.py
Articles = Articles()

# index route
@app.route("/")
def index():
    return render_template("home.html")


# About route
@app.route("/about")
def about():
    return render_template("about.html")


# list all articles route
@app.route("/articles")
def articles():
    return render_template("articles.html", articles=Articles)


# Single article route
@app.route("/article/<string:id>/")
def article(id):
    return render_template("article.html", id=id)


# Register form class template
class RegisterForm(Form):
    name = StringField("Name", [validators.Length(min=1, max=50)])
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=50)])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords do not match"),
        ],
    )
    confirm = PasswordField("Confirm Password")


# Register - sign up route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO  users(name,email,username,password) VALUES (%s,%s,%s,%s)",
            (name, email, username, password),
        )
        mysql.connection.commit()
        cursor.close()

        flash("User registered , Log in to use your account", "success")
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


# Login - sign in route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password_candidate = request.form["password"]

        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            data = cursor.fetchone()
            password = data["password"]

            if sha256_crypt.verify(password_candidate, password):
                session["logged_in"] = True
                session["username"] = username
                flash("You are now logged in", "success")
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid Username or password"
                return render_template("login.html", error=error)

        else:
            error = "User not found"
            return render_template("login.html", error=error)

        cursor.close()

    return render_template("login.html")


# function check user login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("User not found, please login to continue", "danger")
            return redirect(url_for("login"))

    return wrap


# logout route
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("login"))


# dashboard route
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    # app.run()
    # app.run(debug=True,host='0.0.0.0',port="12345")
    app.run(debug=True, port=7000)
