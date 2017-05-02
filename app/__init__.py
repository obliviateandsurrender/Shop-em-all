# Import flask and template operators
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_mail import Mail

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
#CORS(app)
#Bootstrap(app)
# Configurations
app.config.from_object('config')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'notify.shopemall@gmail.com'
app.config['MAIL_PASSWORD'] = 'loveroftime'
ADMINS = ['notify.shopemall@gmail.com']

mail = Mail(app)
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'sellers.seller_login'
# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.buyers.controllers import mod_buyers
from app.sellers.controllers import mod_sellers
# from app.enrolment.controllers import mod_report
from app.product.controllers import mod_product
from app.comments.controllers import mod_comments
from app.cart.controllers import mod_cart
from app.notification.controllers import mod_notification
# Register blueprint(s)
app.register_blueprint(mod_buyers)
app.register_blueprint(mod_sellers)
app.register_blueprint(mod_product)
app.register_blueprint(mod_comments)
app.register_blueprint(mod_cart)
app.register_blueprint(mod_notification)

# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
