from flask import Flask

app = Flask(__name__)

@app.route('/tt')
def home():
    return "Merhaba, Erkan Flask uygulamana hoş geldin!"


@app.route('/hakkinda')
def about():
    return """
        <h1 style = "color:red;">Hakkında</h1>
        <p>Bu bir Flask uygulamasıdır. Flask, Python ile web uygulamaları geliştirmek için kullanılan bir mikro framework'tür.</p>
        <p>Flask, minimal bir yapıya sahip olup, geliştiricilere esneklik ve hız sunar.</p>
        <p>Flask ile hızlı bir şekilde web uygulamaları geliştirebilir, RESTful API'ler oluşturabilir ve daha fazlasını yapabilirsiniz.</p>
        <p>Flask, Jinja2 şablon motorunu kullanarak dinamik içerikler oluşturmanıza olanak tanır.</p>
        <p>Flask, SQLAlchemy gibi popüler veritabanı kütüphaneleri ile entegre edilebilir.</p>
        <p>Flask, geniş bir eklenti ekosistemine sahiptir ve birçok üçüncü taraf kütüphane ile uyumludur.</p>
        <p>Flask, Python'un güçlü özelliklerini kullanarak web uygulamaları geliştirmenizi sağlar.</p>
    """


@app.route('/hakkinda/erkan')
def about_erkan():
    return """

        <title>Hakkında - Erkan</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f4f6f8;
                color: #333;
                margin: 0;
                padding: 40px;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #fff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #007bff;
                text-align: center;
            }
            p {
                font-size: 18px;
                line-height: 1.6;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Erkan</h1>
            <p>Ben Erkan, Python ve Flask ile web uygulamaları geliştirmeyi seven bir yazılım geliştiricisiyim.</p>
            <p>Flask ile hızlı ve etkili web uygulamaları geliştirmek için sürekli olarak kendimi geliştiriyorum.</p>
            <p>Python'un gücünü kullanarak, kullanıcı dostu ve performanslı uygulamalar oluşturmayı hedefliyorum.</p>
            <p>Flask ile çalışmak benim için bir tutku ve bu alanda daha fazla deneyim kazanmayı umuyorum.</p>
        </div>
    </body>

    """



# Eğer bu dosya doğrudan çalıştırıldıysa aşağıdaki kodu çalıştır, başka bir dosyadan import edildiyse çalıştırma.
if __name__ == '__main__':
    app.run(debug=True)


