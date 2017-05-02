from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from app import db,app,login_manager
from flask_cors import CORS
from app.buyers.models import Buyers
from app.product.models import Product
from app.comments.models import Comments
from app.sellers.models import Sellers
from app.cart.models import Cart
from app.notification.models import Notification
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length
# Bootstrap(app)
import easygui
import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mod_buyers = Blueprint('buyers', __name__)
Bootstrap(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me?')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    phone_Number = StringField('Phone Number', validators=[InputRequired(),Length(min=7, max=20)])
    address = TextAreaField('Address', validators=[InputRequired(), Length(min=10, max=200)])
    birthdate = DateField('Birthdate',validators=[InputRequired()], render_kw={"placeholder": "format: yyyy-mm-dd"})

@mod_buyers.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("buyers.showallit"))
    else:
        return render_template('index.html')

@app.before_request
def before_request():
    g.user = current_user

@mod_buyers.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for("buyers.showallit"))
        
        
        # return render_template('dashboard.html', name = current_user.username)
    form = LoginForm()

    if form.validate_on_submit():
        user = Buyers.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # add_sel(form.email.data)
                return redirect(url_for('buyers.showallit'))
                
                
                
        easygui.msgbox("Wrong Credentials", title="Error!")
        return render_template('login.html', form=form)
                    
        
        

    return render_template('login.html', form=form)

@mod_buyers.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        try:
            new_user = Buyers(username=form.username.data, email=form.email.data, password=hashed_password, phone_Number=form.phone_Number.data, address=form.address.data, birthdate=form.birthdate.data)
            #print ("abc")
            add_sel(form.email.data)
            #print ("abc")
            db.session.add(new_user)
            db.session.commit()
            easygui.msgbox("New User Successfully Created", title="Success")
            return redirect(url_for('buyers.login'))
            
        except:
            return render_template('signup.html', form=form)

                        
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@mod_buyers.route('/logout')
@login_required
def logout():
    g.user = None
    session.clear()
    logout_user()
    return redirect(url_for('buyers.index'))


@mod_buyers.route('/addComment', methods = ['POST','GET'])
# @login_required
def addComment():
    if request.method =='POST':
        
        product_id=request.form['proid']
        body=request.form['body']
        user_id=request.form['buyerid']
        

        product = Product.query.filter_by(id = product_id).first()
        
        try:
            print(product)    
            comment = Comments(user_id= user_id,  body = body, product_id=product_id)
            db.session.add(comment)
            db.session.commit()
            print("add")
            return redirect(url_for('buyers.showprod')+'?prodid='+product_id)    
            
        except:
            easygui.msgbox("Failed to add comment", title="Error!")
        
            
       
    return redirect(url_for('buyers.showallit'))    

@mod_buyers.route('/showallitems',methods=['GET','POST'])
@login_required
def showallit():
    array=Product.query.all()
    return render_template("buyerproduct.html",product=array)

@mod_buyers.route('/product', methods=['GET'])
def showprod():
    prod_id=request.args['prodid']
    print(prod_id)
    prod=Product.query.filter_by(id=prod_id).first()
    #return "<h1>True</h1>"  ;
    #print(prod.name)
    #print(prod.price)
    #print(current_user.username)
    commenti=Comments.query.filter_by(product_id=prod_id)
    array=Comments.query.all()
    print(array)
    # print(array[0].product_id)
    # print(commenti.body)
    return render_template('product.html',product=prod,current_user=current_user,comment=commenti)
 
@mod_buyers.route('/addtocart',methods=['POST','GET'])
@login_required
def addcart():
    if request.method =='POST':

        buyer_id=request.form['buyer_id']
        product_id=request.form['product_id']
        quantity=request.form['quantity']
        name=request.form['name']
        type1=request.form['window']
    else:
        buyer_id=request.args.get('buyer_id')
        product_id=request.args.get('product_id')
        quantity=request.args.get('quantity')
        name=request.args.get('name')
        type1=request.args.get('window')
        
    prod=Product.query.filter_by(id=product_id).first()
    print(quantity)
    amount=int(quantity)*prod.price
    if int(quantity) > prod.stock:
        easygui.msgbox("Limited Stock :Please select less items and see product details for stock related things", title="Error")
        # return redirect(url_for('buyers.addcart')+'?buyer_id='+buyer_id+'&product_id='+product_id+'&quantity='+quantity+'&name='+name)    
        return redirect(url_for('buyers.showallit'))    

        
    else:
        status=True
        try:
            cart=Cart(buyer_id=buyer_id,product_id=product_id,quantity=quantity,amount=amount,status=status,name=name)
            db.session.add(cart)
            db.session.commit()
            print("added to cart")
            if type1 =='menu':
                return redirect(url_for('buyers.showallit'))
            else:
                return redirect(url_for('buyers.viewcart'))
            

        except:
            easygui.msgbox("Coudnt add due to internal error", title="Error!")
            if type1 =='menu':
                return redirect(url_for('buyers.showallit'))
            else:
                return redirect(url_for('buyers.viewcart'))
            
            




@mod_buyers.route('/viewcart',methods=['POST','GET'])
@login_required
def viewcart():
    buyer_id=current_user.id

    array=Cart.query.filter_by(buyer_id=buyer_id)
    return render_template('cart.html',product=array)

    

@mod_buyers.route('/deletefromcart',methods=['GET','POST'])
@login_required
def delcart():
    id=request.form['id']
    cart=Cart.query.filter_by(id=id).first()
    try:

        db.session.delete(cart)
        db.session.commit()
        return redirect(url_for('buyers.viewcart'))
    except:
        print("Couldnt delete")
        return redirect(url_for('buyers.viewcart'))
# print(array[0].product_id)
# print(commenti.body)
ca = []
# print(array[0].product_id)
# print(commenti.body)
#           
@mod_buyers.route('/updatecart',methods=['GET','POST'])
def updcart():
    id=request.form['id']
    print(id)
    new_stock=request.form['quantity']

    cart=Cart.query.filter_by(id=id).first()
    print(cart)
    prod_id=cart.product_id
    print(int(prod_id))
    pro=Product.query.filter_by(id=prod_id).first()
    # print(pro)
    if int(new_stock) <= pro.stock:
        cart.amount=(cart.amount/cart.quantity)*int(new_stock)
        
        cart.quantity=int(new_stock)
        
        try:
            db.session.commit()
            print('update')
            return redirect(url_for('buyers.viewcart'))
        except:
            return redirect(url_for('buyers.viewcart'))

    else:
        easygui.msgbox("Please add less than the current stock", title="More in demand less in stock")
        
        return redirect(url_for('buyers.viewcart'))

@mod_buyers.route('/searchbytag',methods=['GET','POST'])
def searchbytag():
    if request.method=='POST':
        tag=request.form['tag']
    else:
        tag=request.args.get('tag')

    print(tag)        
    prod=Product.query.all()
    ans=[]
    for i in prod:
        tagi=i.tags
        array=tagi.split(',')
        print(array)
               
        if tag in array:
            
            print('found')
            ans.append(i)
        else:
            print('notfound')

    if len(ans) is not 0:
        return render_template("buyerproduct.html",product=ans)

    else:
        easygui.msgbox("No such item found", title="Error!")

        return redirect(url_for('buyers.showallit'))



@mod_buyers.route('/category/<category>',methods=['GET','POST'])
def cat(category):
    return redirect(url_for('buyers.categ')+'?category='+category)

@mod_buyers.route('/category',methods=['GET','POST'])
def categ():
    #print(ca)
    category=request.args.get('category')
    array = Product.query.filter_by(category=category)
    #print("hi")
    return render_template("category.html",product=array)

@mod_buyers.route('/buynow',methods=['GET','POST'])
def buynow():
    buyer_id=current_user.id
    email = current_user.email
    array=Cart.query.filter_by(buyer_id=buyer_id)
    amount=0
    flag=0
    temp=0

    print("Buy now")
    for i in array:
        flag=0

        id=i.buyer_id
        pid=i.product_id
        quantity=i.quantity
        produ=Product.query.filter_by(id=pid).first()
        if quantity > produ.stock:
            i.quantity=produ.stock
            flag=1
            temp=1
        produ.stock=produ.stock-quantity
        amount=amount+quantity
        if flag is 0:
            db.session.delete(i)

            
    '''MY_ADDRESS = 'notify.shopemall@gmail.com'
    PASSWORD = 'loveroftime'

    
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()

    message = 'Thanks for Buying products from shomemall'

    print(message)

    msg['From'] = MY_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Thanks"

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)
    del msg 

    s.quit()

# if __name__ == '__main__':
    # main()'''   

    db.session.commit()   
    
    
    easygui.msgbox("Congrats!You have just made the right choice", title="We have just become richer")
    
    if temp is 0:
        easygui.msgbox("Congrats!You have just made the right choice!! please continue and make us more richer", title="We have just become richer")
        return redirect(url_for('buyers.showallit'))
    else:
        easygui.msgbox("Please recheck your cart as some items are less in stock due to huge demand!! be fast this time", title="We have just become richer but can become more")

        return redirect(url_for('buyers.viewcart'))

def add_sel(email):
    #print ("bcdef")
    seller = Sellers(username="kanay12345", email=email, password="shritishma", phone_Number=28936923621836, website="8368329136326183.com")
    #print ("bcde")
    db.session.add(seller)
    db.session.commit()
    #   print ("bcd")
    return

@mod_buyers.route('/sendemailnotification',methods=['GET','POST'])
def sendemail():
    if request.method =='GET':
        pid=request.args.get("pid")
        bid=request.args.get("bid")
    else:
        pid=request.form['pid']
        bid=request.form['bid']    
    product=Product.query.filter_by(id=pid).first()
    
    if product.stock is not 0:
        easygui.msgbox("Sorry the item is currently in stock! But not for longer!!", title="In stock item")
        
        return redirect(url_for('buyers.showprod')+'?prodid='+pid)

    else:
        noti=Notification(buyer_id=bid,product_id=pid)
        db.session.add(noti)
        db.session.commit()
        easygui.msgbox("You will recieve the notification <soon!></soon!>", title="We have just become richer")
        return redirect(url_for('buyers.showprod')+'?prodid='+pid)

   








    
                


        


    
