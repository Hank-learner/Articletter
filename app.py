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

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "yourpasswordhere"
app.config["MYSQL_DB"] = "articletter"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
# mysql initialization
mysql = MySQL(app)

Articles = Articles()


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    return render_template("articles.html", articles=Articles)


@app.route("/article/<string:id>/")
def article(id):
    return render_template("article.html", id=id)


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

        flash("User registered , Log in to use your account","success")
        return redirect(url_for('index'))

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.secret_key='secret123'
    # app.run()
    # app.run(debug=True,host='192.168.43.171',port="19309")
    app.run(debug=True)
