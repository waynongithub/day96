from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.app_context().push() # Required with Flask-SQLAlchemy 3.0 and above

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    asset_name = db.Column(db.String(20), nullable=False)
    cm_id = db.Column(db.Integer, nullable=True) # coinmarketcap id
    cg_id = db.Column(db.Integer, nullable=True) # coingecko id
    date_bought = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float, nullable=True)
    current_price = db.Column(db.Float, nullable=True)
    current_value = db.Column(db.Float, nullable=True)
    pl = db.Column(db.Float, nullable=True)


@app.route('/')
def home():
    assets = Asset.query.all()
    return render_template('index.html', assets=assets)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        string_date= request.form.get('date_bought')
        datetime_obj =  datetime.strptime(string_date, '%Y-%m-%d').date()
        asset = Asset(
            ticker=request.form.get('ticker').upper(),
            asset_name=request.form.get('asset_name'),
            # cm_id=request.form.get('ticker'),
            # cg_id=request.form.get('ticker'),
            date_bought=datetime_obj,
            amount=request.form.get('amount'),
            price=request.form.get('price'),
            currency=request.form.get('currency'),
            value=request.form.get('value'),
        )
        db.session.add(asset)
        db.session.commit()
        return redirect( url_for('home'))
    else:
        return render_template('add.html')


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    asset = Asset.query.filter_by(id=id).first()
    if request.method == "POST":
        string_date = request.form.get('date_bought')
        datetime_obj = datetime.strptime(string_date, '%Y-%m-%d').date()
        print(f"type date={type(datetime_obj)}")

        ticker = request.form.get('ticker').upper()
        print(f"ticker={ticker}, type-{type(ticker)}")
        # asset.ticker="kak",
        # asset.asset_name=request.form.get('asset_name'),
        # asset.cm_id=request.form.get('ticker'),
        # asset.cg_id=request.form.get('ticker'),
        # asset.date_bought=datetime_obj,
        # asset.amount=request.form.get('amount'),
        # asset.price=request.form.get('price'),
        # asset.currency=request.form.get('currency'),
        asset.value=999,
        db.session.commit()
        return redirect( url_for('home'))
    else:
        return render_template('edit.html', asset=asset, id=id)







if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)