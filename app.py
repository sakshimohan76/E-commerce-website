from flask import Flask,render_template, url_for,request, flash, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image, ImageFilter

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ecommerce.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
app.secret_key='sakshimohanshoppingapp'

currentWorkingDirectory = os.getcwd()
uploader=os.path.join(currentWorkingDirectory, 'static\\pictures')
app.config['UPLOAD_FOLDER']=uploader

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
MAX_SIZE = (32, 32) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

with app.app_context():
    db=SQLAlchemy(app)    

class Customer(db.Model,UserMixin):
    emailC=db.Column(db.String(200), primary_key=True, unique=True)
    usernameC=db.Column(db.String(200),nullable=False)
    passwordC=db.Column(db.String(200)) 
    passwordC=db.Column(db.String(200)) 
    seller_emailS=db.Column(db.String, db.ForeignKey('seller.emailS')) 
    assigned_seller = db.relationship('Seller', backref='customer')
    products=db.relationship('Products', backref='products_customer',lazy=True)
    cart=db.relationship('Cart', backref='patient',lazy=True)
    def get_id(self):
        return self.emailC

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pName = db.Column(db.String(200), nullable=False)
    category= db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(20000), nullable=False)
    price= db.Column(db.Integer, nullable=False)
    filename = db.Column(db.Text, nullable=False, unique=False)
    customer_emailC = db.Column(db.String, db.ForeignKey('customer.emailC', ondelete='CASCADE'))
    seller_emailS = db.Column(db.String, db.ForeignKey('seller.emailS', ondelete='CASCADE'))
    customer_obj = db.relationship('Customer', backref=db.backref('customer_products', cascade='all, delete-orphan'))
    seller_obj = db.relationship('Seller', backref=db.backref('seller_products', cascade='all, delete-orphan'))

class Seller(db.Model,UserMixin):
    emailS=db.Column(db.String(200), primary_key=True, unique=True)
    usernameS=db.Column(db.String(200),nullable=False)
    passwordS=db.Column(db.String(200))  
    is_seller = db.Column(db.Boolean, default=False)
    pi = db.relationship('PI', backref='pi_seller')
    products=db.relationship('Products', backref='products_seller',lazy=True)
    def get_id(self):
        return self.emailS

class PI(db.Model,UserMixin):
    bank= db.Column(db.Integer,primary_key=True)
    bName=db.Column(db.String(200)) 
    contact= db.Column(db.Integer)
    address=db.Column(db.String(200))
    seller_emailS = db.Column(db.String(200), db.ForeignKey('seller.emailS',ondelete='CASCADE'))

class Cart(db.Model,UserMixin):
    id = db.Column(db.String(250), primary_key=True)
    pName = db.Column(db.String(200), nullable=False)
    category= db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(20000), nullable=False)
    price= db.Column(db.Integer, nullable=False)
    filename = db.Column(db.Text, nullable=False, unique=False)
    customer_emailC = db.Column(db.String, db.ForeignKey('customer.emailC', ondelete='CASCADE'))
    
login_manager=LoginManager()
login_manager.login_view='index'    
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    customer = Customer.query.get(email)
    if customer:
        return customer
    seller = Seller.query.get(email)
    if seller:
        return seller
    
    return None

@app.route("/",methods=['GET','POST'])
def index():
    allPro = Products.query.all()
    return render_template("index.html",allPro=allPro)

@app.route("/signUpC", methods=['POST','GET'])
def signUpC():
    if request.method=='POST':
       usernameC=request.form.get('usernameC') 
       emailC=request.form.get('emailC') 
       existing_customer = Seller.query.filter_by(emailS=emailC).first()
       if existing_customer:
           flash('Email is already associated with a seller account.', category='error')
           return render_template("signUpC.html")
       passwordC1=request.form.get('passwordC1')
       passwordC2=request.form.get('passwordC2')

       customer=Customer.query.filter_by(emailC=emailC).first()
       if customer:
            flash('User already exists!', category='error')
            return redirect('/logInC')
       elif len(usernameC)<3:
            flash('Name must be greater than 2 characters!' ,category='error')
            return render_template("signUpC.html")
       elif len(emailC)<5:  
            flash('Email must be greater than 4 characters!' ,category='error')
       elif len(passwordC1)<5:  
            flash('Password must be greater than 4 characters!' ,category='error')  
       elif passwordC1!=passwordC2:  
            flash('Passwords do not match!' ,category='error')   
       else:
            cnew_user=Customer(emailC=emailC, usernameC=usernameC, passwordC=generate_password_hash(passwordC1, method='sha256'))
            db.session.add(cnew_user)
            db.session.commit()
            login_user(cnew_user)
            flash('Account created!', category='success')  
            return redirect('/logInC')
    return render_template("signUpC.html")

@app.route("/logInC", methods=['POST','GET'])
def logInC():
    if request.method=='POST':
       emailC=request.form.get('emailC') 
       passwordC=request.form.get('passwordC1')

       customer=Customer.query.filter_by(emailC=emailC).first()
       if customer:
            if check_password_hash(customer.passwordC, passwordC):
                login_user(customer)
                allPro = Products.query.all()
                return render_template("homeForC.html", allPro=allPro)
            else:
                flash('Password is incorrect!', category='error')
       else:
            flash('User does not exist! Create new user here.', category='error') 
            return redirect(url_for('signUpC'))    
    return render_template("logInC.html")

@app.route("/homeForC")
def homeForC():
    allPro = Products.query.all()
    return render_template("homeForC.html",allPro=allPro)

@app.route("/addToCart/<int:id>", methods=['POST','GET'])
def addToCart(id):
    if request.method == 'POST':
        product = Products.query.get(id)
        if product:
            cart_item = Cart.query.filter_by(id=current_user.emailC+":"+str(id), customer_emailC=current_user.emailC).first()
            if cart_item:
                flash("Item is already in the cart.", category='success' )
            else:
                cart_item = Cart(id=current_user.emailC+":"+str(id), pName=product.pName,
                category=product.category,
                desc=product.desc,
                price=product.price,
                filename=product.filename,
                customer_emailC=current_user.emailC)
                db.session.add(cart_item)
                db.session.commit()
    return redirect(url_for('cart'))

@app.route("/cart")
def cart():
    allPro = Cart.query.filter_by(customer_emailC=current_user.emailC).all()
    return render_template("addToCart.html", allPro=allPro)

def calculate_cart_total(allPro):
    total = 0
    for item in allPro:
        total += item.price
    return total

@app.route('/buy', methods=['GET', 'POST'])
def checkout():
    allPro = Cart.query.filter_by(customer_emailC=current_user.emailC).all()
    total = calculate_cart_total(allPro)
    if request.method == 'POST':
        return redirect('/confirmation')
    return render_template("buy.html", allPro=allPro, total=total)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method=="POST":
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        card = request.form.get('card')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        if name != None and address != None and phone != None and card != None and expiry != None and cvv != None:
            Cart.query.filter_by(customer_emailC=current_user.emailC).delete()
            db.session.commit()
            flash("Congratulations! Order confirmed. See you soon!", category='success')
        return redirect(url_for('pay'))
    return render_template("pay.html")

@app.route("/signUpS", methods=['POST','GET'])
def signUpS():
    if request.method=='POST':
       usernameS=request.form.get('usernameS') 
       emailS=request.form.get('emailS') 
       existing_customer = Customer.query.filter_by(emailC=emailS).first()
       if existing_customer:
           flash('Email is already associated with a customer account.', category='error')
           return render_template("signUpS.html")
       passwordS1=request.form.get('passwordS1')
       passwordS2=request.form.get('passwordS2')

       seller=Seller.query.filter_by(emailS=emailS).first()
       if seller:
            flash('User already exists!', category='error')
            return redirect('/logInS')
       elif len(usernameS)<3:
            flash('Name must be greater than 2 characters!' ,category='error')
            return render_template("signUpS.html")
       elif len(emailS)<5:  
            flash('Email must be greater than 4 characters!' ,category='error')
       elif len(passwordS1)<5:  
            flash('Password must be greater than 4 characters!' ,category='error')  
       elif passwordS1!=passwordS2:  
            flash('Passwords do not match!' ,category='error')   
       else:  
            snew_user = Seller(emailS=emailS, usernameS=usernameS, passwordS=generate_password_hash(passwordS1, method='sha256'))
            db.session.add(snew_user)
            db.session.commit()
            login_user(snew_user)
            flash('Account created!', category='success')
            return redirect('/logInS')
    return render_template("signUpS.html")

@app.route("/PI", methods=['POST', 'GET'])
@login_required
def addPI():
    if request.method == 'POST':
        address = request.form.get('address')
        bank = request.form.get('bank')
        bName = request.form.get('bName')
        contact = request.form.get('contact')
        new_pi =PI(address=address, bank=bank, contact=contact, bName=bName,seller_emailS=current_user.emailS)
        db.session.add(new_pi)
        db.session.commit()
        return redirect(url_for('sPI'))
    return redirect(url_for('sPI'))

@app.route("/showPI",methods=['GET','POST'])
def sPI():
    allPI=PI.query.filter_by(seller_emailS=current_user.emailS).all()
    return render_template("PI.html",allPI=allPI)   

@app.route("/logInS", methods=['POST','GET'])
def logInS():
    if request.method=='POST':
       emailS=request.form.get('emailS') 
       passwordS=request.form.get('passwordS1')

       seller=Seller.query.filter_by(emailS=emailS).first()
       if seller:
            if check_password_hash(seller.passwordS, passwordS):
                login_user(seller)
                return redirect(url_for('sell'))

            else:
                flash('Password is incorrect!', category='error')
       else:
            flash('User does not exist! Create new user here.', category='error') 
            return redirect(url_for('signUpS'))    
    return render_template("logInS.html")

@login_required
@app.route('/sell')
def sell():
    allPro = Products.query.filter_by(seller_emailS=current_user.emailS).all()        
    return render_template("sell.html", allPro=allPro, seller=current_user)

@login_required
@app.route("/addProduct", methods=['POST', 'GET'])
def addProduct():
    if request.method == 'POST':
        pName = request.form.get('product')
        desc = request.form.get('desc')
        price = request.form.get('price')            
        file = request.files['file1']
        category=request.form.get('category')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)               
            filepath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), filename)
            file.save(filepath)
            thumbpath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbs'), filename)
            thumb = Image.open(file)
            thumb = thumb.filter(ImageFilter.BLUR)
            thumb.thumbnail(MAX_SIZE)
            thumb.save(thumbpath)

        new_pro = Products(pName=pName, desc=desc, price=price,category=category,filename=filename) 
        new_pro.seller_emailS= current_user.emailS
        db.session.add(new_pro)
        db.session.commit()
        return redirect('sell')
    return render_template("addProduct.html")

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    pro=Products.query.filter_by(id=id).first()
    db.session.delete(pro)
    db.session.commit()
    return redirect('/sell')

@app.route('/remove/<int:id>')
def remove(id):
    pro=Cart.query.filter_by(id=current_user.emailC+":"+id).first()
    db.session.delete(pro)
    db.session.commit()
    return redirect('/cart')

@app.route('/del/<int:bank_id>')
def delete_pi(bank_id):
    p = PI.query.filter_by(bank=bank_id).first()
    db.session.delete(p)
    db.session.commit() 
    return redirect('/PI')

@app.route('/edit/<int:id>',methods=['POST','GET'], endpoint='edit')
def edit(id):
    if request.method=='POST':
        pName=request.form.get('product')
        desc = request.form.get('desc')
        price = request.form.get('price')
        category=request.form.get('category')
        file = request.files['file1'] 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)               
            filepath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), filename)
            file.save(filepath)
            thumbpath = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], 'thumbs'), filename)
            thumb = Image.open(file)
            thumb = thumb.filter(ImageFilter.GaussianBlur(radius=75))
            thumb.thumbnail(MAX_SIZE)
            thumb.save(thumbpath)
        else:
            pro = Products.query.filter_by(id=id).first()
            filename = pro.filename    
        
        pro = Products.query.filter_by(id=id).first()
        pro.pName=pName
        pro.desc=desc
        pro.price=price
        pro.category=category
        pro.filename=filename
        db.session.commit()
        flash('Product updated!',category='success')
        return render_template("update.html",pro=pro)
        
    pro = Products.query.filter_by(id=id).first()
    return render_template("update.html",pro=pro)

if __name__=="__main__":
    app.run(debug=True)