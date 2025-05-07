from functools import wraps
from flask import Flask , render_template, flash, redirect,session, url_for, logging,request
from flask_mysqldb import MySQL # MySQL veritabanı ile bağlantı kurmak için flask_mysqldb kütüphanesini kullanıyoruz.
from wtforms import Form, StringField, TextAreaField, PasswordField, validators # wtforms kütüphanesi ile form işlemleri yapacağız.
from passlib.hash import sha256_crypt # passlib kütüphanesi ile şifreleme işlemi yapacağız.
import os # Ortam değişkenlerini kullanmak için os kütüphanesini kullanıyoruz.
import time # Zaman işlemleri için time kütüphanesini kullanıyoruz.
import email_validator # email_validator kütüphanesi ile email doğrulama işlemi yapacağız.



#====================Kullanıcı giirş decoratoru========================================================================================
def login_required(f):
    @wraps(f) # Decorator fonksiyonu oluşturuyoruz.
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("Bu sayfayı görüntülemek için öncelikle giriş yapmalısınız!", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


#====================Kayıt formu Start===============================================================================================
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

#====================Kayıt formu End===============================================================================================


app = Flask(__name__)


# Ortam değişkeninden alın veya rastgele bir değer üretin
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24)

#====================DB baglantı islemleri ===============================================================================================

app.config['MYSQL_HOST'] = 'localhost' # MySQL sunucusunun adresi
app.config['MYSQL_USER'] = 'admin' # MySQL kullanıcı adı
app.config['MYSQL_PASSWORD'] = 'Erkan1205/*-+' # MySQL şifresi
app.config['MYSQL_DB'] = 'coder_erkan_blog' # MySQL veritabanı adı
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # MySQL veritabanına bağlanmak için kullanılacak cursor sınıfı
mysql = MySQL(app) # MySQL veritabanına bağlanmak için mysql nesnesi oluşturuyoruz.


#====================Anasayfa Islemleri===============================================================================================

@app.route("/")
def index():
        # Kullanıcı oturumu kontrolü
    if "logged_in" in session:
        # Kullanıcı giriş yapmışsa, session'dan kullanıcı adını al
        userName = session.get("username")
        
        #Kullanıcı giriş yapmışsa, veritabanından makaleleri al

                
        return render_template("index.html", username=userName)
        
    else:
        # Eğer kullanıcı giriş yapmamışsa, "Misafir" olarak göster
        return render_template("index.html",username="Misafir" )
    #return render_template("index.html" , answer=2)

#====================About Islemleri===============================================================================================
@app.route("/about")
def about():
    return render_template("about.html")


#Dinamic URL Yapısı
# Flask, dinamik URL yapısını destekler. URL'de değişkenler kullanarak dinamik içerik oluşturabiliriz.
@app.route("/article/<string:article_id>")
def article(article_id):
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,)) # article_id'ye göre makaleyi veritabanından alıyoruz.
    if result > 0:
        article = cursor.fetchone()
        # Makaleyi render ediyoruz.
        return render_template("article.html", article=article)
    else:
        flash("Böyle bir makale bulunamadı!", "danger")
        cursor.close()
        return redirect(url_for("index"))   
    


#====================REGISTER Islemleri============================================================================================
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


#====================LOGIN Islemleri===============================================================================================

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




#====================LOGOUT Islemleri===============================================================================================
@app.route("/logout")
@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def logout():
        session.clear() # Oturumu temizliyoruz.    
        flash("Çıkış işlemi başarılı!", "success") # Başarılı çıkış mesajı gösteriyoruz.
        return redirect(url_for("index")) # Anasayfaya yönlendiriyoruz.
    
#====================Kullanıcı Profil Islemleri====================================================================================
@app.route("/dashboard")
@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def dashboard():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM articles WHERE author = %s", (session["username"],)) # Kullanıcı adı ile veritabanında arama yapıyoruz.
        articles = cursor.fetchall() # Kullanıcı adı ile eşleşen verileri alıyoruz.
        cursor.close() # Veritabanı bağlantısını kapatıyoruz.
        if articles:
            # Eğer makale varsa, veritabanından makaleleri alıyoruz.
            articles_list = list(articles)
            articles_list.sort(key=lambda x: x['id'], reverse=True)
            # Makaleleri render ediyoruz.
            return render_template("dashboard.html", articles=articles_list)
        else:
            # Eğer makale yoksa, boş bir liste döndürüyoruz.
            articles = []
            cursor.close()
        return render_template("dashboard.html")

    



#====================Makale Ekleme Islemleri===============================================================================================
@app.route("/addarticle", methods=["GET", "POST"])
@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def add_article():
    form = ArticleForm(request.form) # Makale ekleme formunu oluşturuyoruz.
    if request.method == "POST" and form.validate(): # Eğer form geçerli ise
        # Formdan gelen verileri alıyoruz.
        title = form.title.data
        content = form.content.data
        # Veritabanına makale ekleme işlemi
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO articles(title,author, content) VALUES(%s,%s, %s)", (title,session["username"], content))
        mysql.connection.commit()
        cursor.close()
        flash("Makale başarıyla eklendi!", "success") # Başarılı ekleme mesajı gösteriyoruz.
        return redirect(url_for("dashboard")) # Makale ekleme işlemi başarılı ise anasayfaya yönlendiriyoruz.
    else:
        # Eğer form geçerli değilse veya GET isteği ise formu gösteriyoruz.
        if form.errors:
            for error in form.errors.values():
                flash(error[0], "danger")
        return render_template("addarticle.html", form=form)

#====================Makale EKLEME FORMU==============================================================================================

class ArticleForm(Form):
    title = StringField("Makale Başlığı", [validators.Length(min=5, max=100)]) # Makale başlığı için minimum 5, maksimum 100 karakter uzunluğunda olmalıdır.
    content = TextAreaField("Makale İçeriği", [validators.Length(min=10)]) # Makale içeriği için minimum 10 karakter uzunluğunda olmalıdır.



@app.route("/articles")
@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def articles():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles")
    if result > 0:
        # Eğer makale varsa, veritabanından makaleleri alıyoruz.
        articles = cursor.fetchall()
        # Makaleleri ters sırada sıralıyoruz (en son eklenen makale en üstte olacak şekilde)
        articles_list = list(articles)
        articles_list.sort(key=lambda x: x['id'], reverse=True)
        # Makaleleri render ediyoruz.
    
        return(render_template("articles.html" , articles=articles_list))
    else:
        # Eğer makale yoksa, boş bir liste döndürüyoruz.
        articles = []
    cursor.close()
    return render_template("articles.html", articles=articles_list)


if __name__ == "__main__":
    app.run(debug=True)