from app import nexusdb

class Comments (nexusdb.Model):
    __tablename__ = 'comments'
    id = nexusdb.Column(nexusdb.Integer, primary_key=True)
    user_name = nexusdb.Column(nexusdb.Integer, nexusdb.ForeignKey('users.id'))
    post_id = nexusdb.Column(nexusdb.Integer, nexusdb.ForeignKey('posts.id'))
    text = nexusdb.Column(nexusdb.Text, nullable=False)