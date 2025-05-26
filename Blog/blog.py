from functools import wraps
from flask import Flask, render_template, flash, redirect, session, url_for, logging, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import os
import time
import email_validator
from dotenv import load_dotenv
from datetime import datetime

#====================Kullanıcı giirş decoratoru========================================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            flash("Bu sayfayı görüntülemek için öncelikle giriş yapmalısınız!", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

#====================Kayıt formu Start===============================================================================================
class RegisterForm(Form):
    name = StringField("İsim Soyisim", [validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", [validators.Length(min=4, max=25)])
    email = StringField("Email Adresi", [validators.Email(message="Lütfen geçerli bir email adresi giriniz!")])
    password = PasswordField("Şifre", validators=[
        validators.DataRequired(message="Şifre boş olamaz"),
        validators.EqualTo(fieldname="confirm", message="Şifreler uyuşmuyor"),
        validators.Length(min=6, max=35, message="Şifre en az 6 karakter olmalıdır")
    ])
    confirm = PasswordField("Şifre Tekrar")

app = Flask(__name__)

# Secret key from environment variables
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MySQL veritabanı yapılandırması
load_dotenv()

# MySQL bağlantı bilgileri
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

# Veritabanı modelleri
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    articles = db.relationship('Article', backref='author_rel', lazy=True)

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)
    author = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)

# Veritabanını oluştur
with app.app_context():
    db.create_all()
    # Admin kullanıcısı yoksa oluştur
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            name='Admin',
            username='admin',
            email='admin@example.com',
            password=sha256_crypt.encrypt('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

# Örnek olarak index route'unu güncelleyelim:
@app.route("/")
def index():
    featured_articles = Article.query.filter_by(is_approved=True).order_by(Article.created_date.desc()).limit(3).all()
    is_admin = False
    if "logged_in" in session:
        user = User.query.filter_by(username=session["username"]).first()
        is_admin = user.is_admin if user else False
    
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

# Örnek olarak register route'unu güncelleyelim:
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
                flash("Bu kullanıcı adı zaten kullanılıyor!", "danger")
                return render_template("register.html", form=form)
        if User.query.filter_by(email=email).first():
                flash("Bu email adresi zaten kayıtlı!", "danger")
                return render_template("register.html", form=form)
        
        new_user = User(name=name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Kayıt işlemi başarılı!", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)