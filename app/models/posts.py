from app import nexusdb

class Posts (nexusdb.Model):
    __tablename__ = 'posts'
    id = nexusdb.Column(nexusdb.Integer, primary_key=True)
    user_name = nexusdb.Column(nexusdb.Integer, nexusdb.ForeignKey('users.id'))
    text = nexusdb.Column(nexusdb.Text, nullable=False)
    name = nexusdb.Column(nexusdb.String(64), nullable=False)
    board = nexusdb.Column(nexusdb.String(64), nullable=False)