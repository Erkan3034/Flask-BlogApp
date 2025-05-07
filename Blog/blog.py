from flask import Flask , render_template, flash, redirect,session, url_for, logging,request
from flask_mysqldb import MySQL # MySQL veritabanı ile bağlantı kurmak için flask_mysqldb kütüphanesini kullanıyoruz.
from wtforms import Form, StringField, TextAreaField, PasswordField, validators # wtforms kütüphanesi ile form işlemleri yapacağız.
from passlib.hash import sha256_crypt # passlib kütüphanesi ile şifreleme işlemi yapacağız.
import os # Ortam değişkenlerini kullanmak için os kütüphanesini kullanıyoruz.
import time # Zaman işlemleri için time kütüphanesini kullanıyoruz.
import email_validator # email_validator kütüphanesi ile email doğrulama işlemi yapacağız.




#====================Kayıt formu Start============================
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

#====================Kayıt formu End============================


app = Flask(__name__)


# Ortam değişkeninden alın veya rastgele bir değer üretin
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

#====================DB baglantı islemleri ============================

app.config['MYSQL_HOST'] = 'localhost' # MySQL sunucusunun adresi
app.config['MYSQL_USER'] = 'admin' # MySQL kullanıcı adı
app.config['MYSQL_PASSWORD'] = 'Erkan1205/*-+' # MySQL şifresi
app.config['MYSQL_DB'] = 'coder_erkan_blog' # MySQL veritabanı adı
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # MySQL veritabanına bağlanmak için kullanılacak cursor sınıfı
mysql = MySQL(app) # MySQL veritabanına bağlanmak için mysql nesnesi oluşturuyoruz.


#====================Anasayfa Islemleri============================

@app.route("/")
def index():
        # Kullanıcı oturumu kontrolü
    if "logged_in" in session:
        # Kullanıcı giriş yapmışsa, session'dan kullanıcı adını al
        userName = session.get("username")
        
        #Kullanıcı giriş yapmışsa, veritabanından makaleleri al
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
                
        return render_template("index.html", username=userName ,articles=articles)
        
    else:
        # Eğer kullanıcı giriş yapmamışsa, "Misafir" olarak göster
        return render_template("index.html",username="Misafir" )
    #return render_template("index.html" , answer=2)

#====================About Islemleri============================
@app.route("/about")
def about():
    return render_template("about.html")


#Dinamic URL Yapısı
# Flask, dinamik URL yapısını destekler. URL'de değişkenler kullanarak dinamik içerik oluşturabiliriz.
@app.route("/article/<string:article_id>")
def article(article_id):
    return render_template("index.html", article_id=article_id)


#====================REGISTER Islemleri============================
@app.route("/register" , methods=["GET" , "POST"])
def register():
    form = RegisterForm(request.form) # Form nesnesi oluşturuyoruz, form verilerini alıyoruz.
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)  # Şifreyi sha256_crypt ile şifreliyoruz.
        
        # Check if username or email already exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userName, email FROM users WHERE userName = %s OR email = %s", (username, email))
        user = cursor.fetchone()
        
        if user:
            if user['userName'] == username:
                flash("Bu kullanıcı adı zaten kullanılıyor!", "danger")
            if user['email'] == email:
                flash("Bu email adresi zaten kayıtlı!", "danger")
            cursor.close()
            return render_template("register.html", form=form)
        else:
            cursor = mysql.connection.cursor() # MySQL veritabanına bağlanıyoruz.
            cursor.execute("INSERT INTO users(name, username, email, password) VALUES(%s, %s, %s, %s)", (name, username, email, password))
            mysql.connection.commit()
            cursor.close() # Veritabanı bağlantısını kapatıyoruz.
            if cursor.execute:
                flash("Kayıt işlemi başarılı!", "success")
            else:
                flash("Kayıt işlemi başarısız!", "danger")
            return redirect(url_for("login")) # Kayıt işlemi başarılı ise giriş sayfasına yönlendiriyoruz.
            #return render_template("succededRegistration.html")
    else:
        return render_template("register.html" , form=form)


#====================LOGIN Islemleri============================

@app.route("/login" , methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username") # Kullanıcı adı formdan alınıyor.
        password = request.form.get("password") # Şifre formdan alınıyor.
        #print(username)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT userName,password FROM users WHERE userName = %s", (username,)) # Kullanıcı adı ile veritabanında arama yapıyoruz.
        user = cursor.fetchone() # Kullanıcı adı ile eşleşen veriyi alıyoruz.(sözlük olarak veri gelir)
        
        if user and sha256_crypt.verify(password, user['password']): # Eğer kullanıcı adı ve şifre doğru ise
            #------------Session işlemleri ------------------
            session["logged_in"] = True # Kullanıcı giriş yapmış olarak işaretleniyor.
            session["username"] = username # Kullanıcı adı oturumda saklanıyor.
            flash("Giriş başarılı!", "success")
            return redirect(url_for("index"))
        else:
            flash("Kullanıcı adı veya şifre hatalı!", "danger")
            return render_template("login.html")
    return render_template("login.html")




#====================LOGOUT Islemleri============================
@app.route("/logout")
def logout():
    session.clear() # Oturumu temizliyoruz.
    flash("Çıkış işlemi başarılı!", "success") # Başarılı çıkış mesajı gösteriyoruz.

    return redirect(url_for("index")) # Anasayfaya yönlendiriyoruz.

if __name__ == "__main__":
    app.run(debug=True)