from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wsedSDuuitdUfi7ygRDr5u4353'  
db = SQLAlchemy(app)

# User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100))
    collections = db.relationship('Collection', backref='user', lazy=True)

# Collection model
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('CollectionItem', backref='collection', lazy=True)

# Item model
class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    value = db.Column(db.String(50))
    tag = db.Column(db.String(50))
    description = db.Column(db.Text)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/delete/<int:coll_id>")
def delete(coll_id):
    collection = Collection.query.get_or_404(coll_id)
    
    # Delete all items in the collection first (to avoid foreign key errors)
    for item in collection.items:
        db.session.delete(item)
    
    db.session.delete(collection)
    db.session.commit()
    return redirect(url_for('userhome'))

@app.route("/delete_item/<int:item_id>")
def delete_item(item_id):
    collection = CollectionItem.query.get_or_404(item_id)
    db.session.delete(collection)
    db.session.commit()
    return redirect(url_for('userhome'))
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('userhome'))
        else:
            flash("Login failed. Check credentials.", 'error')
    return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        check = Users.query.filter_by(username=request.form['username']).first()
        if check:
            flash("Username already exists. Please choose a different one.", 'error')
            return redirect(url_for('signup'))
        user = Users(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('userhome'))
    return render_template("signup.html")


@app.route("/userhome")
def userhome():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = Users.query.get_or_404(session['user_id'])
    return render_template("userhome.html", collections=user.collections, user=user)

@app.route("/view_collection/<int:collection_id>")
def view_collection(collection_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    collection = Collection.query.get_or_404(collection_id)
    if collection.user_id != session['user_id']:
        return "Unauthorized", 403
    return render_template('collections.html', collection=collection)

@app.route("/add_to_collection/<int:collection_id>", methods=['POST'])
def add_to_collection(collection_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    collection = Collection.query.get_or_404(collection_id)
    if collection.user_id != session['user_id']:
        return "Unauthorized", 403

    item = CollectionItem(
        name=request.form['name'],
        category=request.form['category'],
        value=request.form['value'],
        description=request.form['description'],
        tag=request.form['tag'],
        collection_id=collection.id
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('view_collection', collection_id=collection_id))

@app.route("/add_collection", methods=['POST'])
def add_collection():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    collection = Collection(
        name=request.form["title"],
        user_id=session['user_id']
    )
    db.session.add(collection)
    db.session.commit()
    return redirect(url_for('userhome'))

if __name__ == '__main__':
    app.run(debug=True)
