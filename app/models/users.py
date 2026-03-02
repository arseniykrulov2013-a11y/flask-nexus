from app import nexusdb
from flask_login import UserMixin

class Users (nexusdb.Model, UserMixin):
    __tablename__ = 'users'
    id = nexusdb.Column(nexusdb.Integer, primary_key=True)
    login = nexusdb.Column(nexusdb.String(128), nullable=False)
    password = nexusdb.Column(nexusdb.String(255), nullable=False)
    description = nexusdb.Column(nexusdb.String(255), default="Нет описания...")
    is_admin = nexusdb.Column(nexusdb.String(18), default="FALSE")