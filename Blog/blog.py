from flask import Flask , render_template, flash, redirect,session, url_for, logging,request
from flask_mysqldb import MySQL # MySQL veritabanı ile bağlantı kurmak için flask_mysqldb kütüphanesini kullanıyoruz.

from wtforms import Form, StringField, TextAreaField, PasswordField, validators # wtforms kütüphanesi ile form işlemleri yapacağız.

from passlib.hash import sha256_crypt # passlib kütüphanesi ile şifreleme işlemi yapacağız.


#Kullanıcı Kayıt formu start
class RegisterForm(Form):
    name = StringField("İsim Soyisim" , [validators.Length(min=4 , max=25)])
    username = StringField("Kullanıcı Adı" , [validators.Length(min=4 , max=25)])
    email = StringField("Email Adresi" , [validators.Email(message="Lütfen geçerli bir email adresi giriniz!")])
    # Email adresinin geçerli olup olmadığını kontrol ediyoruz.
    password = PasswordField("Şifre" ,validators= [
        validators.DataRequired(message="Şifre boş olamaz"),
        validators.EqualTo(fieldname="confirm", message="Şifreler uyuşmuyor"), # Şifrelerin eşleşip eşleşmediğini kontrol ediyoruz.
        validators.Length(min=6, max=35, message="Şifre en az 6 karakter olmalıdır") # Şifrenin uzunluğunu kontrol ediyoruz.
    ])
    confirm = PasswordField("Şifre Tekrar")

# Kullanıcı Kayıt formu end


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost' # MySQL sunucusunun adresi
app.config['MYSQL_USER'] = 'admin' # MySQL kullanıcı adı
app.config['MYSQL_PASSWORD'] = 'Erkan1205/*-+' # MySQL şifresi
app.config['MYSQL_DB'] = 'coder_erkan_blog' # MySQL veritabanı adı
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # MySQL veritabanına bağlanmak için kullanılacak cursor sınıfı
mysql = MySQL(app) # MySQL veritabanına bağlanmak için mysql nesnesi oluşturuyoruz.




@app.route("/")
def index():
    articles = [
        { 
            "Id" : 1,
            "title": "Flask Basics",
            "content": "Learn the basics of Flask, a micro web framework for Python"
        },
        {
            "Id" : 2,
            "title": "Flask Templates",
            "content": "Learn how to use templates in Flask to render dynamic content"
        },
        {
            "Id" : 3,
            "title": "Flask Forms",
            "content": "Learn how to handle forms in Flask applications"
        },
        ]
    return render_template("index.html", articles=articles)
    #return render_template("index.html" , answer=2)


@app.route("/about")
def about():
    return render_template("about.html")


#Dinamic URL Yapısı
# Flask, dinamik URL yapısını destekler. URL'de değişkenler kullanarak dinamik içerik oluşturabiliriz.
@app.route("/article/<string:article_id>")
def article(article_id):
    return render_template("index.html", article_id=article_id)


# Kullanıcı Kayıt işlemi
@app.route("/register" , methods=["GET" , "POST"])
def register():
    form = RegisterForm(request.form) # Form nesnesi oluşturuyoruz, form verilerini alıyoruz.
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor() # MySQL veritabanına bağlanıyoruz.
        cursor.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
        mysql.connection.commit()
        cursor.close() # Veritabanı bağlantısını kapatıyoruz.
        flash("Kayıt işlemi başarılı!", "success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html" , form=form)


if __name__ == "__main__":
    app.run(debug=True)