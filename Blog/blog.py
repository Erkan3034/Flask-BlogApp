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
app.config['MYSQL_USER'] = 'root' # MySQL kullanıcı adı
app.config['MYSQL_PASSWORD'] = 'Erkan1205/*-+' # MySQL şifresi
app.config['MYSQL_DB'] = 'coder_erkan_blog' # MySQL veritabanı adı
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # MySQL veritabanına bağlanmak için kullanılacak cursor sınıfı
mysql = MySQL(app) # MySQL veritabanına bağlanmak için mysql nesnesi oluşturuyoruz.


#====================Anasayfa Islemleri===============================================================================================

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE is_approved = TRUE ORDER BY created_date DESC LIMIT 3")
    featured_articles = cursor.fetchall()
    is_admin = False
    if "logged_in" in session:
        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
        user = cursor.fetchone()
        is_admin = user['is_admin'] if user else False
    cursor.close()
    if "logged_in" in session:
        return render_template("index.html", 
                             username=session["username"],
                             featured_articles=featured_articles,
                             is_admin=is_admin)
    else:
        return render_template("index.html",
                             username="Misafir",
                             featured_articles=featured_articles,
                             is_admin=False)

#====================About Islemleri===============================================================================================
@app.route("/about")
def about():
    return render_template("about.html")


#Dinamic URL Yapısı
# Flask, dinamik URL yapısını destekler. URL'de değişkenler kullanarak dinamik içerik oluşturabiliriz.
@app.route("/article/<string:article_id>")
@login_required  # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def article(article_id):
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,)) # article_id'ye göre makaleyi veritabanından alıyoruz.
    if result > 0:
        article = cursor.fetchone()
        cursor.close()
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
    next_url = request.args.get("next")
    if request.method == "GET" and next_url:
        flash("Bu makaleyi okumak için önce giriş yapmalısınız!", "warning")
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
            if next_url:
                return redirect(next_url)
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
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    is_admin = user['is_admin'] if user else False
    # Kendi makaleleri
    cursor.execute("SELECT * FROM articles WHERE author = %s ORDER BY id DESC", (session["username"],))
    own_articles = cursor.fetchall()
    # Admin ise diğer kullanıcıların makaleleri
    other_articles = []
    if is_admin:
        cursor.execute("SELECT * FROM articles WHERE author != %s ORDER BY id DESC", (session["username"],))
        other_articles = cursor.fetchall()
    cursor.close()
    return render_template("dashboard.html", articles=own_articles, other_articles=other_articles, is_admin=is_admin)

    



#====================Makale Ekleme Islemleri===============================================================================================
@app.route("/addarticle", methods=["GET", "POST"])
@login_required
def add_article():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO articles(title,author, content, is_approved) VALUES(%s,%s, %s, %s)", (title,session["username"], content, False))
        mysql.connection.commit()
        cursor.close()
        flash("Makaleniz başarıyla gönderildi. Admin onayından sonra yayınlanacaktır!", "info")
        return redirect(url_for("dashboard"))
    else:
        if form.errors:
            for error in form.errors.values():
                flash(error[0], "danger")
        return render_template("addarticle.html", form=form)

#====================Makale EKLEME FORMU==============================================================================================

class ArticleForm(Form):
    title = StringField("Makale Başlığı", [validators.Length(min=5, max=100)]) # Makale başlığı için minimum 5, maksimum 100 karakter uzunluğunda olmalıdır.
    content = TextAreaField("Makale İçeriği", [validators.Length(min=10)]) # Makale içeriği için minimum 10 karakter uzunluğunda olmalıdır.



@app.route("/articles")
@login_required
def articles():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM articles WHERE is_approved = TRUE")
    if result > 0:
        articles = cursor.fetchall()
        articles_list = list(articles)
        articles_list.sort(key=lambda x: x['id'], reverse=True)
        return(render_template("articles.html" , articles=articles_list))
    else:
        articles = []
    cursor.close()
    return render_template("articles.html", articles=articles_list)



#====================Makale Silme Islemleri===============================================================================================
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    is_admin = user['is_admin'] if user else False
    if is_admin:
        query = "SELECT * FROM articles WHERE id = %s"
        result = cursor.execute(query, (id,))
    else:
        query = "SELECT * FROM articles WHERE author = %s AND id = %s"
        result = cursor.execute(query, (session["username"], id))
    if result > 0:
        query2 = "DELETE FROM articles WHERE id = %s"
        cursor.execute(query2, (id,))
        mysql.connection.commit()
        cursor.close()
        flash("Makale başarıyla silindi!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Böyle bir makale bulunamadı veya yetkiniz yok!", "danger")
        cursor.close()
        return redirect(url_for("index"))


#====================Makale Güncelleme Islemleri===============================================================================================
@app.route("/edit/<string:id>", methods=["GET", "POST"])
@login_required
def update(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    is_admin = user['is_admin'] if user else False
    if request.method == "GET":
        if is_admin:
            query3 = "SELECT * FROM articles WHERE id = %s"
            result = cursor.execute(query3, (id,))
        else:
            query3 = "SELECT * FROM articles WHERE author = %s AND id = %s"
            result = cursor.execute(query3, (session["username"], id))
        if result > 0:
            article = cursor.fetchone()
            form = ArticleForm(request.form)
            form.title.data = article["title"]
            form.content.data = article["content"]
            cursor.close()
            return render_template("update.html", form=form)
        else:
            flash("Böyle bir makale bulunamadı veya yetkiniz yok!", "danger")
            cursor.close()
            return redirect(url_for("index"))
    elif request.method == "POST":
        form = ArticleForm(request.form)
        new_title = form.title.data
        new_content = form.content.data
        if is_admin:
            query4 = "UPDATE articles SET title = %s, content = %s WHERE id = %s"
            cursor.execute(query4, (new_title, new_content, id))
        else:
            query4 = "UPDATE articles SET title = %s, content = %s WHERE author = %s AND id = %s"
            cursor.execute(query4, (new_title, new_content, session["username"], id))
        mysql.connection.commit()
        cursor.close()
        flash("Makale başarıyla güncellendi!", "success")
        return redirect(url_for("dashboard"))
    else:
        if form.errors: 
            for error in form.errors.values():
                flash(error[0], "danger")
            return render_template("update.html", form=form, article=article)

    

#====================Arama URL==============================================================================================
@app.route("/search", methods=["GET", "POST"])
@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile yönlendiriyoruz.
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()  
        search_query = "SELECT * FROM articles WHERE title LIKE %s OR content LIKE %s"
        search_result = cursor.execute(search_query, ('%' + keyword + '%', '%' + keyword + '%'))
        if search_result > 0:
            articles = cursor.fetchall()
            articles_list = list(articles)
            articles_list.sort(key=lambda x: x['id'], reverse=True)
            return render_template("articles.html", articles=articles_list)
        else:
            flash("Aradığınız kelimeye uygun makale bulunamadı!", "danger")
            return redirect(url_for("index"))
            
    elif request.method == "GET":
        return redirect(url_for("index"))



#====================İletişim Sayfası========================================================================================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# 3. Admin paneli: Onay bekleyen makaleler
@app.route("/admin/articles")
@login_required
def admin_articles():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    if not user or not user['is_admin']:
        flash("Bu sayfaya erişim yetkiniz yok!", "danger")
        return redirect(url_for("index"))
    cursor.execute("SELECT * FROM articles ORDER BY created_date DESC")
    all_articles = cursor.fetchall()
    cursor.close()
    return render_template("admin_articles.html", articles=all_articles)

# 4. Admin makale onaylama/ret
@app.route("/admin/approve/<int:article_id>")
@login_required
def approve_article(article_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    if not user or not user['is_admin']:
        flash("Bu işlemi yapmaya yetkiniz yok!", "danger")
        return redirect(url_for("index"))
    cursor.execute("UPDATE articles SET is_approved = TRUE WHERE id = %s", (article_id,))
    mysql.connection.commit()
    cursor.close()
    flash("Makale onaylandı!", "success")
    return redirect(url_for("admin_articles"))

@app.route("/admin/reject/<int:article_id>")
@login_required
def reject_article(article_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    if not user or not user['is_admin']:
        flash("Bu işlemi yapmaya yetkiniz yok!", "danger")
        return redirect(url_for("index"))
    cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    mysql.connection.commit()
    cursor.close()
    flash("Makale silindi!", "info")
    return redirect(url_for("admin_articles"))

@app.route('/admin-panel')
@login_required
def admin_panel():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session["username"],))
    user = cursor.fetchone()
    if not user or not user['is_admin']:
        flash("Bu sayfaya erişim yetkiniz yok!", "danger")
        return redirect(url_for("index"))
    cursor.close()
    return render_template("admin_panel.html")

if __name__ == "__main__":
    app.run(debug=True)