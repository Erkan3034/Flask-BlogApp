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




app2 = Flask(__name__)


app2.config['MYSQL_HOST'] = 'localhost' # MySQL sunucusunun adresi
app2.config['MYSQL_USER'] = 'admin' # MySQL kullanıcı adı
app2.config['MYSQL_PASSWORD'] = 'Erkan1205/*-+' # MySQL şifresi
app2.config['MYSQL_DB'] = 'coder_erkan_blog' # MySQL veritabanı adı
app2.config['MYSQL_CURSORCLASS'] = 'DictCursor' # MySQL veritabanına bağlanmak için kullanılacak cursor sınıfı
mysql = MySQL(app2) # MySQL veritabanına bağlanmak için mysql nesnesi oluşturuyoruz.




@app2.route("/")
def index():

    article = dict()
    article["title"] = "Flask ile Web Geliştirme"
    article["content"] = "Flask, Python ile web uygulamaları geliştirmek için kullanılan bir mikro framework'tür. Flask, minimal bir yapıya sahip olup, geliştiricilere esneklik ve özelleştirme imkanı sunar."
    article["author"] = "Erkan Turgut"
    article["date"] = "2025-04-27"
    return render_template("index.html" , article=article)



@app2.route("/about")
def about():
    return render_template("about.html")

@app2.route("/blog")
def blog():
    sayi =15
    return render_template("blog.html" , number = sayi)

@app2.route("/register")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app2.run(debug=True)