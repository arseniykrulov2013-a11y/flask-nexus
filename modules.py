from main import db, lm, app, UserMixin

class Users (db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), default="Нет описания...")
    is_admin = db.Column(db.String(18), default="FALSE")

class Posts (db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    board = db.Column(db.String(64), nullable=False)

class Comments (db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    text = db.Column(db.Text, nullable=False)

def CREATE_ALL():
    with app.app_context():
        db.create_all()

CREATE_ALL()
