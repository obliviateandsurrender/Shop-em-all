from app.sellers.models import Sellers
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
from flask_wtf import FlaskForm 

from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from app import db,app,login_manager,ADMINS
from app.product.models import Product
from app.buyers.models import Buyers
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField,SelectField,IntegerField,FloatField,FileField
import easygui
from PIL import Image
import os
from os.path import expanduser
from flask_mail import Message
from app import mail
from app.notification.models import Notification
	
mod_sellers = Blueprint('sellers', __name__)
#Bootstrap(app)

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me?')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    phone_Number = StringField('Phone Number', validators=[InputRequired(),Length(min=7, max=20)])
    website = TextAreaField('Website', validators=[InputRequired(), Length(min=10, max=200)])

class NewForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=50)])
    category= SelectField('Category', choices =[('clothes','Clothes'),('shoes','Shoes'),('books','Books and Stationary'),('sports','Sport Accessories'),('electronics','Electronics Goods and accessories'),('mobile','Mobile and accessories')] , validators = [InputRequired()])
    tags = StringField('Tags', validators=[InputRequired(), Length(min=4, max=30)])
    description= StringField('Description', validators=[InputRequired(), Length(min=4, max=100)])
    stock = IntegerField('Stock', validators=[InputRequired()])
    price=FloatField('Price',validators=[InputRequired()])
    # img=FileField(validators = [InputRequired()])
       
@app.before_request
def before_request():
    g.user = current_user

@mod_sellers.route('/')
def index():
    if g.user is not None:
        return redirect(url_for('sellers.dash'))
    else:
        return render_template('index.html')

@login_manager.user_loader
def load_user(seller_id):
    return Sellers.query.get(int(seller_id))

@mod_sellers.route('/sellerlogin',methods=['GET','POST'])
def seller_login():
    if g.user is not None and g.user.is_authenticated:
        return render_template('seller_dashboard.html', name = current_user.username)
        
    form=LoginForm()
    
    if form.validate_on_submit():
        user=Sellers.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                user.authenticated = True
                login_user(user,remember=form.remember.data)
                return redirect(url_for('sellers.dash'))
        		
                # return render_template('seller_dashboard.html', name=current_user.username)
        easygui.msgbox("Wrong Credentials", title="Error!")
        return render_template('seller_login.html', form=form)

    return render_template('seller_login.html',form=form)	

@mod_sellers.route('/dashboard',methods=['GET','POST'])
@login_required
def dash():
	return render_template('seller_dashboard.html', name=current_user.username)

@mod_sellers.route('/sellersignup',methods=['GET','POST'])
def seller_signup():
	form=RegisterForm()
	if form.validate_on_submit():

		hashed_password = generate_password_hash(form.password.data, method='sha256')
        
		try:
			new_user = Sellers(username=form.username.data, email=form.email.data, password=hashed_password, phone_Number=form.phone_Number.data, website=form.website.data)
			db.session.add(new_user)
			db.session.commit()
			easygui.msgbox("New User Successfully Created", title="simple gui")
			return redirect(url_for('sellers.seller_login'))
			
		except:
			return render_template('seller_signup.html', form=form)
    
	return render_template('seller_signup.html', form=form)

@mod_sellers.route('/sellerlogout')
@login_required
def seller_logout():
    g.user = None
    session.clear()
    logout_user()
    return redirect(url_for('sellers.index'))

@mod_sellers.route('/addnewproduct',methods=['POST','GET'])
@login_required
def addnew():
    form=NewForm()
    if form.validate_on_submit():
        try:
            user1 = Product(str(form.name.data), int(form.stock.data),float(form.price.data),str(form.description.data),str(form.category.data),str(form.tags.data),current_user.id)
            #print("added1");
            db.session.add(user1)
            db.session.commit()
            #print("Added 1")
            img=request.form['file']
            home = expanduser("~")
            path_image = home + "/" + img
            img1 = Image.open(path_image)
            #print('I')
            dir = os.getcwd()
            print(dir)
            dir1 = os.path.join(dir, 'app/static/')
            # print(dir1)
            filename = str(user1.id) + '.jpg'
            imageurl = dir1 + filename
            # print(imageurl)
            img1.save(imageurl)

            easygui.msgbox("Product Successfully added: Add more and earn more", title="Success!")

            return redirect(url_for('sellers.addnew'))	
        except:
            easygui.msgbox("Product Could not be added: PLEASE TRY AGAIN", title="Error!")
            return redirect(url_for('sellers.addnew'))
    return render_template('newproduct.html', form=form)

@mod_sellers.route('/showallproducts',methods=['GET','POST'])
def showall():
	userid=current_user.id
	array=Product.query.filter_by(seller_id=userid).all()
	print(userid)
	print(Product.query.all()) 
	print(array)

	for i in array:
		print(i)
	print("Hi this is correct")
	return render_template('sellerproduct.html',product=array)
	

@mod_sellers.route('/updatestock',methods=['GET','POST'])
@login_required
def upstock():
    prod_id=request.args.get('id')
    print(prod_id)
    new_stock=request.args.get('quantity')
    prod=Product.query.filter_by(id=prod_id).first()
    if prod.stock == 0:
        noti=Notification.query.filter_by(product_id=prod_id).all()
        print("In notifi")
        for i in noti:
            buyer=Buyers.query.filter_by(id=i.buyer_id).first()
            email=buyer.email
            print(email)
            msg = Message("HOORAH item is in stcok", sender=ADMINS[0], recipients=[email])
            msg.body = "Hey he item you were looking in shopemall.com is back in stock !! do visit before it again goes away"
            msg.html = "Same as above"
            mail.send(msg)
    print("Done")        
    prod.stock=new_stock
    db.session.commit()
    userid=current_user.id
    array=Product.query.filter_by(seller_id=userid).all()
    return render_template('sellerproduct.html',product=array)

@mod_sellers.route('/deleteproduct',methods=['GET','POST'])
@login_required
def delprod():
	prod_id=request.args.get('id')
	
	prod=Product.query.filter_by(id=prod_id).first()
	
	db.session.delete(prod)
	os.system("rm /home/kanay/itws_all_assignments/major_project/Alpha_Shopping-portal_Beta_phase/app/static"+prod_id)
	db.session.commit()
	
	userid=current_user.id
	array=Product.query.filter_by(seller_id=userid).all()
	return render_template('sellerproduct.html',product=array)

	



















































































