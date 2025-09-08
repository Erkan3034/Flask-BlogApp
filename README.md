# 🚀 Erkan Turgut Kişisel Blog Sitesi

Bu proje, Flask framework'ü kullanılarak geliştirilmiş modern bir kişisel blog sitesidir. Full Stack web geliştirme, AI/ML projeleri ve teknoloji yazıları paylaşmak amacıyla tasarlanmıştır.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Veritabanı Yapısı](#-veritabanı-yapısı)
- [API Endpoints](#-api-endpoints)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## ✨ Özellikler

### 👤 Kullanıcı Yönetimi
- **Kullanıcı Kaydı**: Email doğrulaması ile güvenli kayıt sistemi
- **Giriş/Çıkış**: Session tabanlı authentication
- **Profil Yönetimi**: Kullanıcı dashboard'u ile kişisel makale yönetimi
- **Rol Tabanlı Erişim**: Admin ve normal kullanıcı rolleri

### 📝 İçerik Yönetimi
- **Makale Yazma**: Rich text editor ile makale oluşturma
- **Makale Onay Sistemi**: Admin onayı ile yayınlama
- **Kategori Yönetimi**: Teknik konular için etiket sistemi
- **Arama ve Filtreleme**: İçerik keşfi için gelişmiş arama

### 🔧 Admin Paneli
- **İçerik Moderasyonu**: Makale onaylama/reddetme
- **Kullanıcı Yönetimi**: Admin yetkisi verme/alma
- **Site Yönetimi**: Navbar ve ana sayfa içerik yönetimi
- **İstatistikler**: Dashboard ile site metrikleri

### 🎨 Kullanıcı Deneyimi
- **Responsive Tasarım**: Mobil-first yaklaşım ile modern UI
- **Bootstrap 5**: Modern ve hızlı arayüz komponenleri
- **Dark/Light Theme**: (Geliştirilme aşamasında)
- **Sosyal Medya Entegrasyonu**: GitHub ve LinkedIn bağlantıları

## 🛠 Teknoloji Yığını

### Backend
- **Flask 2.3.3**: Python web framework'ü
- **MySQL**: İlişkisel veritabanı yönetim sistemi
- **Flask-MySQLdb**: MySQL veritabanı bağlantısı
- **WTForms**: Form doğrulama ve işleme
- **Passlib**: Güvenli şifre hashleme (SHA256)

### Frontend
- **HTML5 & CSS3**: Modern web standartları
- **Bootstrap 5**: Responsive UI framework
- **Bootstrap Icons**: Vektör ikon kütüphanesi
- **Jinja2 Templates**: Dinamik içerik render'lama

### Güvenlik & Doğrulama
- **Email Validator**: Email format doğrulaması
- **CSRF Protection**: Cross-site request forgery koruması
- **Session Management**: Güvenli oturum yönetimi
- **SQL Injection Prevention**: Parametreli sorgular

### Deployment & DevOps
- **Gunicorn**: Production WSGI server
- **Python-dotenv**: Environment variables yönetimi
- **Secrets Module**: Güvenli rastgele key üretimi

## 🚀 Kurulum

### Ön Gereksinimler
- Python 3.8+
- MySQL 5.7+ veya MariaDB
- Git

### Adım 1: Repository'yi Klonlayın
```bash
git clone https://github.com/yourusername/Flask-BlogApp.git
cd Flask-BlogApp/Blog
```

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: MySQL Veritabanını Ayarlayın
```sql
CREATE DATABASE coder_erkan_blog;
USE coder_erkan_blog;

-- Kullanıcılar tablosu
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Makaleler tablosu
CREATE TABLE articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author) REFERENCES users(username)
);
```

### Adım 5: Veritabanı Bağlantısını Yapılandırın
`blog.py` dosyasındaki veritabanı ayarlarını kendi MySQL bilgilerinizle güncelleyin:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'coder_erkan_blog'
```

### Adım 6: Uygulamayı Çalıştırın
```bash
python blog.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 📖 Kullanım

### İlk Admin Kullanıcısı Oluşturma
1. Normal kayıt işlemini tamamlayın
2. MySQL'de kullanıcının `is_admin` değerini `TRUE` olarak güncelleyin:
```sql
UPDATE users SET is_admin = TRUE WHERE username = 'your_username';
```

### Makale Yönetimi
- **Yeni Makale**: Dashboard > "Makale Ekle" butonu
- **Makale Düzenleme**: Kendi makalelerinizi dashboard'dan düzenleyebilirsiniz
- **Admin Onayı**: Admin kullanıcılar tüm makaleleri onaylayabilir

### Admin Paneli Erişimi
Admin kullanıcılar şu özelliklerine erişebilir:
- `/admin-panel`: Site yönetim paneli
- `/admin/articles`: Tüm makaleleri görüntüleme ve yönetme
- Makale onaylama/reddetme işlemleri

## 📁 Proje Yapısı

```
Flask-BlogApp/
└── Blog/
    ├── blog.py                 # Ana Flask uygulaması
    ├── requirements.txt        # Python bağımlılıkları
    ├── static/                 # Statik dosyalar
    │   └── css/               # CSS dosyaları
    ├── templates/             # HTML şablonları
    │   ├── layout.html        # Ana layout şablonu
    │   ├── index.html         # Ana sayfa
    │   ├── about.html         # Hakkımda sayfası
    │   ├── articles.html      # Makale listesi
    │   ├── article.html       # Tekil makale görünümü
    │   ├── dashboard.html     # Kullanıcı paneli
    │   ├── admin_panel.html   # Admin paneli
    │   ├── login.html         # Giriş sayfası
    │   ├── register.html      # Kayıt sayfası
    │   └── includes/          # Ortak şablon parçaları
    │       ├── navbar.html    # Navigasyon menüsü
    │       ├── messages.html  # Flash mesajları
    │       └── form_helpers.html # Form yardımcıları
    └── assets/
        └── img/              # Görsel dosyalar
```

## 🗄 Veritabanı Yapısı

### Users Tablosu
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | INT (PK) | Kullanıcı benzersiz kimliği |
| name | VARCHAR(100) | Kullanıcının tam adı |
| username | VARCHAR(50) | Benzersiz kullanıcı adı |
| email | VARCHAR(100) | Benzersiz email adresi |
| password | VARCHAR(255) | Hashlenmiş şifre (SHA256) |
| is_admin | BOOLEAN | Admin yetkisi durumu |
| created_date | TIMESTAMP | Kayıt tarihi |

### Articles Tablosu
| Alan | Tip | Açıklama |
|------|-----|----------|
| id | INT (PK) | Makale benzersiz kimliği |
| title | VARCHAR(200) | Makale başlığı |
| content | TEXT | Makale içeriği |
| author | VARCHAR(50) | Yazar kullanıcı adı (FK) |
| is_approved | BOOLEAN | Onay durumu |
| created_date | TIMESTAMP | Oluşturulma tarihi |

## 🛣 API Endpoints

### Genel Sayfalar
- `GET /` - Ana sayfa
- `GET /about` - Hakkımda sayfası
- `GET /contact` - İletişim sayfası

### Kimlik Doğrulama
- `GET/POST /register` - Kullanıcı kaydı
- `GET/POST /login` - Kullanıcı girişi
- `GET /logout` - Kullanıcı çıkışı

### Makale İşlemleri
- `GET /articles` - Onaylanmış makaleler listesi
- `GET /article/<id>` - Tekil makale görüntüleme
- `GET/POST /add-article` - Yeni makale ekleme
- `GET/POST /edit/<id>` - Makale düzenleme
- `GET /delete/<id>` - Makale silme

### Kullanıcı Paneli
- `GET /dashboard` - Kullanıcı dashboard'u

### Admin İşlemleri
- `GET /admin-panel` - Admin paneli
- `GET /admin/articles` - Tüm makaleler yönetimi
- `GET /admin/approve/<id>` - Makale onaylama
- `GET /admin/reject/<id>` - Makale reddetme

## 🔒 Güvenlik Özellikleri

### Authentication & Authorization
- **Session-based Authentication**: Flask session yönetimi
- **Role-based Access Control**: Admin ve user rolleri
- **Login Required Decorator**: Korumalı route'lar için

### Data Protection
- **Password Hashing**: SHA256 ile güvenli şifre saklama
- **SQL Injection Prevention**: Parametreli MySQL sorguları
- **CSRF Protection**: Form güvenliği
- **Input Validation**: WTForms ile veri doğrulama

### Security Headers
- **Secure Session Keys**: Secrets modülü ile rastgele key üretimi
- **Environment Variables**: Hassas bilgilerin güvenli saklanması

## 🎨 UI/UX Özellikleri

### Modern Tasarım
- **Bootstrap 5**: Responsive ve modern UI komponenleri
- **Custom CSS**: Marka renkleri ve özel stiller
- **Bootstrap Icons**: Vektör ikon seti
- **Gradient Backgrounds**: Modern görsel efektler

### Responsive Design
- **Mobile-First**: Mobil cihazlar için optimize edilmiş
- **Flexible Grid**: Bootstrap grid sistemi
- **Adaptive Components**: Ekran boyutuna göre uyarlanabilen bileşenler

### User Experience
- **Flash Messages**: Kullanıcı geri bildirimleri
- **Loading States**: Kullanıcı etkileşim göstergeleri
- **Intuitive Navigation**: Kolay navigasyon menüsü
- **Search & Filter**: İçerik keşfi özellikleri

## 🚀 Deployment

### Production Ayarları
```python
# Production için güvenlik ayarları
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Gunicorn ile çalıştırma
gunicorn -w 4 -b 0.0.0.0:5000 blog:app
```

### Environment Variables
```bash
# .env dosyası oluşturun
MYSQL_HOST=your_host
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
MYSQL_DB=your_database
SECRET_KEY=your_secret_key
```

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Geliştirme Rehberi
- PEP 8 Python kodlama standartlarını takip edin
- Yeni özellikler için test yazın
- Commit mesajlarında açıklayıcı başlıklar kullanın
- Documentation güncellemelerini unutmayın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

**Erkan Turgut**
- GitHub: [@Erkan3034](https://github.com/Erkan3034)
- LinkedIn: [erkanturgut1205](https://www.linkedin.com/in/erkanturgut1205)



⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
