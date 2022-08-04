from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from  cloudipsp import Api, Checkout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img = db.Column(db.Text, nullable=False)
    disp = db.Column(db.String(100), nullable=False)
    proc = db.Column(db.String(100), nullable=False)
    memor = db.Column(db.String(200), nullable=False)
    sdmem = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title


@app.route("/")
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data=items)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/buy/<int:id>")
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        img = request.form['img']
        disp = request.form['disp']
        proc = request.form['proc']
        memor = request.form['memor']
        sdmem = request.form['sdmem']
        price = request.form['price']

        item = Item(title=title, price=price, img=img, disp=disp, proc=proc, memor=memor, sdmem=sdmem)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "ERROR DB"
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
