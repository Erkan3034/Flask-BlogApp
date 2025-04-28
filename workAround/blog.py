from flask import Flask , render_template

app2 = Flask(__name__)


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

@app2.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app2.run(debug=True)