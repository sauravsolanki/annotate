from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # This is a one-to-many relationship
    # A puppy can have many toys
    # toys = db.relationship('Toy',backref='puppy',lazy='dynamic')
    user_id = db.relationship('UserDetails',backref='User',lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)


class UserDetails(db.Model):
    # Create a table in the db
    __tablename__ = 'users_details'

    id = db.Column(db.Integer, primary_key = True)
    # Connect the toy to the puppy that owns it.
    # We use puppies.id because __tablename__='puppies'
    # puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    image_url = db.Column(db.String(128), unique=True, index=True)
    datetime = db.Column(db.String(128))

    def __init__(self,user_id,image_url, datetime):
        self.user_id=user_id
        self.image_url=image_url
        self.datetime=datetime
